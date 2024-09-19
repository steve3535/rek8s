from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
import httpx

from .models import WithdrawalRequest, WithdrawalResponse
from .database import engine, SessionLocal, AtmDB, Base, get_db

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

# Configuration FastAPI
app = FastAPI()

SWITCH_URL = "http://127.0.0.1:8002"



# Endpoint pour le retrait
@app.post('/withdraw', response_model=WithdrawalResponse)
async def withdraw(request: WithdrawalRequest, db: Session = Depends(get_db)):
    transaction_id = str(uuid.uuid4())
    async with httpx.AsyncClient() as client:
        try:
            # Appel au service de traitement de transaction
            response = await client.post(f"{SWITCH_URL}/process_transaction/", json={
                "transaction_id": transaction_id,
                "card_number": request.card_number,
                "amount": request.amount,
                "atm_id": request.atm_id,
                "transaction_type": "withdrawal"
            })

            # Si le service répond avec succès (200 OK)
            if response.status_code == 200:
                data = response.json()
                
                # Vérification supplémentaire sur le contenu de la réponse
                if data.get("status") == "success":
                    db_response = AtmDB(
                        transaction_id=transaction_id,
                        card_number=request.card_number,
                        amount=request.amount,
                        atm_id=request.atm_id,
                        status="success",
                        message="Withdrawal successful",
                        timestamp=datetime.utcnow()
                    )
                    db.add(db_response)
                    db.commit()

                    return WithdrawalResponse(
                        transaction_id=transaction_id,
                        status="success",
                        message="Withdrawal successful",
                        timestamp=datetime.utcnow()
                    )
                else:
                    db_response = AtmDB(
                        transaction_id=transaction_id,
                        card_number=request.card_number,
                        amount=request.amount,
                        atm_id=request.atm_id,
                        status="failed",
                        message="Withdrawal failed",
                        timestamp=datetime.utcnow()
                    )
                    db.add(db_response)
                    db.commit()
                    # Si la réponse du service n'indique pas un succès explicite
                    raise HTTPException(status_code=400, detail="Transaction failed")

            else:
                # Si le service distant renvoie un code d'erreur (ex: 400, 500, etc.)
                raise HTTPException(status_code=response.status_code, detail=f"Switch returned error: {response.text}")

        except httpx.RequestError as e:
            # Rollback en cas de problème
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error communicating with switch: {str(e)}")

# Endpoint de vérification de la santé
@app.get('/health')
async def health_check():
    return {"status": "healthy"}
