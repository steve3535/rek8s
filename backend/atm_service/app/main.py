from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
import httpx
from models import WithdrawalRequest, WithdrawalResponse, AtmDB, TransactionOut
from database import engine, SessionLocal, Base, get_db
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import uvicorn
# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

# Configuration FastAPI
app = FastAPI()
load_dotenv(dotenv_path="/rek8s/backend/.env")
port_atm = int(os.getenv("PORT_ATM", 8008))
port_ni = int(os.getenv("PORT_NI", 8002))
SWITCH_URL = f"http://127.0.0.1:{port_ni}"

#origins = ["http://127.0.0.1:5500",  "http://localhost:5500",  ]

app.add_middleware(
    CORSMiddleware,
    #allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/withdraw/', response_model=WithdrawalResponse)
async def withdraw(request: WithdrawalRequest, db: Session = Depends(get_db)):
    transaction_id = str(uuid.uuid4())
    print(f"Request received: {request}") 
    print("Transaction request validated: ", request)

    async with httpx.AsyncClient() as client:
        try:
            # Appel au service de traitement de transaction
            response = await client.post(f"{SWITCH_URL}/process_transaction/", json={
                "transaction_id": transaction_id,
                "card_number": request.card_number,
                "amount": request.amount,
                "atm_id": request.atm_id,
                "transaction_type": request.transaction_type
            })
            #data = response.json()
            data = response.json()
            print(response.content)

            # Si le service répond avec succès (200 OK)
            if response.status_code == 200:
                #data = response.json()
                
                # Vérification supplémentaire sur le contenu de la réponse
                if data['status'] == "successful":
                    db_response = AtmDB(
                        transaction_id=transaction_id,
                        card_number=request.card_number,
                        amount=request.amount,
                        atm_id=request.atm_id,
                        status=data['status'],
                        message=data['message'],
                        transaction_type=request.transaction_type,  # Ajoutez transaction_type ici
                        timestamp=datetime.utcnow()
                    )
                    db.add(db_response)
                    db.commit()

                    return WithdrawalResponse(
                        transaction_id=transaction_id,
                        status="success",
                        message=request.transaction_type + " successful",
                        transaction_type=request.transaction_type,  # Ajoutez transaction_type ici aussi
                        timestamp=datetime.utcnow()
                    )
                elif  data['status'] == "failed":
                    db_response = AtmDB(
                        transaction_id=transaction_id,
                        card_number=request.card_number,
                        amount=request.amount,
                        atm_id=request.atm_id,
                        status=data['status'],
                        message=data['message'],
                        transaction_type=request.transaction_type,  # Ajoutez transaction_type ici
                        timestamp=datetime.utcnow()
                    )
                    db.add(db_response)
                    db.commit()
                    # Si la réponse du service n'indique pas un succès explicite
                    return WithdrawalResponse(
                        transaction_id=transaction_id,
                        status=data['status'],
                        message=data['message'],
                        transaction_type=request.transaction_type,  # Ajoutez transaction_type ici aussi
                        timestamp=datetime.utcnow()
                    )

            else:
                # Si le service distant renvoie un code d'erreur (ex: 400, 500, etc.)
                raise HTTPException(status_code=response.status_code, detail=f"Switch returned error: {response.text}")

        except httpx.RequestError as e:
            # Rollback en cas de problème
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error communicating with switch: {str(e)}")



@app.get("/showtransactions/", response_model=List[TransactionOut])
def get_transaction(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    transactions = db.query(AtmDB).order_by(AtmDB.timestamp.desc()).offset(skip).limit(limit).all()
    return transactions

# Endpoint de vérification de la santé
@app.get('/health')
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port_atm, reload=True)