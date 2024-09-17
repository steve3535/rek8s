
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
import httpx

from models import WithdrawalRequest, WithdrawalResponse
from database import engine, SessionLocal, AtmDB, Base

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)
# Configuration FastAPI
app = FastAPI()

SWITCH_URL = "http://127.0.0.1:8002"

# Pydantic Models


# Dépendance pour obtenir la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint pour le retrait
@app.post('/withdraw', response_model=WithdrawalResponse)
async def withdraw(request: WithdrawalRequest, db: Session = Depends(get_db)):
    transaction_id = str(uuid.uuid4())
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{SWITCH_URL}/process_transaction/", json={
                "transaction_id": transaction_id,
                "card_number": request.card_number,
                "amount": request.amount,
                "atm_id": request.atm_id,
                "transaction_type": "withdrawal"
            })

            if response.status_code == 200:
                # Persist successful response
                db_response = AtmDB(
                    transaction_id=transaction_id,
                    card_number=request.card_number,
                    amount = request.amount,
                    atm_id=request.atm_id,
                    status="success",
                    message="Withdrawal successful",
                    timestamp=datetime.now()
                )
                db.add(db_response)
                db.commit()

                return WithdrawalResponse(
                    transaction_id=transaction_id,
                    status="success",
                    message="Withdrawal successful",
                    timestamp=datetime.now()
                )
            else:
                # Persist failed response
                db_response = AtmDB(
                    transaction_id=transaction_id,
                    card_number=request.card_number,
                    amount = request.amount,
                    atm_id=request.atm_id,
                    status="failed",
                    message=f"Withdrawal failed: {response.json().get('detail', 'Unknown error')}",
                    timestamp=datetime.now()
                )
                db.add(db_response)
                db.commit()

                return WithdrawalResponse(
                    transaction_id=transaction_id,
                    status="failed",
                    message=f"Withdrawal failed: {response.json().get('detail', 'Unknown error')}",
                    timestamp=datetime.now()
                )

        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error communicating with switch: {str(e)}")

# Endpoint de vérification de la santé
@app.get('/health')
async def health_check():
    return {"status": "healthy"}


