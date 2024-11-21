from fastapi import FastAPI, HTTPException, Depends
from models import TransactionRequest, TransactionResponse, TransactionOut, NiDB
import httpx
from datetime import datetime
from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import uvicorn

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI()
load_dotenv(dotenv_path="/rek8s/.env")
port_ni = int(os.getenv("PORT_NI", 8005))
port_banking = int(os.getenv("PORT_BANKING", 8000))
CORE_BANKING_URL = f"http://localhost:{port_banking}"

# Définir les origines autorisées (peut-être '*' pour autoriser toutes les origines)
#origins = [ "http://127.0.0.1:5500",      "http://localhost:5500",  ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dépendance pour obtenir la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/process_transaction/", response_model=TransactionResponse)
async def process_transaction(request: TransactionRequest, db: Session = Depends(get_db)):
    # Vérification de la carte
    async with httpx.AsyncClient() as client:
        try:
            account_response = await client.get(f"{CORE_BANKING_URL}/accounts/card/{request.card_number}")
            
            if account_response.status_code != 200:
                # Carte invalide
                db_response = NiDB(
                    transaction_id=request.transaction_id,
                    card_number=request.card_number,
                    amount=request.amount,
                    atm_id=request.atm_id,
                    transaction_type=request.transaction_type,
                    status="failed",
                    message="Invalid Card number",
                    timestamp=datetime.now()
                )
                db.add(db_response)
                db.commit()
                return TransactionResponse(
                    transaction_id=request.transaction_id,
                    status="failed",
                    message="Invalid Card number",
                    transaction_type=request.transaction_type,
                    timestamp=datetime.now()
                )
            
            account = account_response.json()

            # Vérification du type de transaction et du solde
            if request.transaction_type == 'withdrawal' and account['balance'] < request.amount:
                # Solde insuffisant
                db_response = NiDB(
                    transaction_id=request.transaction_id,
                    card_number=request.card_number,
                    amount=request.amount,
                    atm_id=request.atm_id,
                    transaction_type=request.transaction_type,
                    status="failed",
                    message="Insufficient funds",
                    timestamp=datetime.now()
                )
                db.add(db_response)
                db.commit()
                return TransactionResponse(
                    transaction_id=request.transaction_id,
                    status="failed",
                    message="Insufficient funds",
                    transaction_type=request.transaction_type,
                    timestamp=datetime.now()
                )
            
            # Appel à l'API des transactions dans le core banking
            response = await client.post(f"{CORE_BANKING_URL}/transactions/", json={
                "id": request.transaction_id,
                "account_id": account['id'],
                "amount": request.amount,
                "transaction_type": request.transaction_type
            })

            if response.status_code == 200:
                # Transaction réussie
                db_response = NiDB(
                    transaction_id=request.transaction_id,
                    card_number=request.card_number,
                    amount=request.amount,
                    atm_id=request.atm_id,
                    transaction_type=request.transaction_type,
                    status="successful",
                    message=f"{request.transaction_type.capitalize()} successful",
                    timestamp=datetime.now()
                )
                db.add(db_response)
                db.commit()
                return TransactionResponse(
                    transaction_id=request.transaction_id,
                    status="successful",
                    message=f"{request.transaction_type.capitalize()} successful",
                    transaction_type=request.transaction_type,
                    timestamp=datetime.now()
                )
            else:
                raise HTTPException(status_code=response.status_code, detail="Transaction failed in core banking")
        
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error communicating with core banking: {str(e)}")


@app.get("/transactions/", response_model=List[TransactionOut])
def get_transaction(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    transactions = db.query(NiDB).order_by(NiDB.timestamp.desc()).offset(skip).limit(limit).all()
    return transactions


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port_ni, reload=True)