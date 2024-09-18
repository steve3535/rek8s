from fastapi import FastAPI, HTTPException, Depends
from models import TransactionRequest, TransactionResponse
import httpx
from datetime import datetime
from database import engine, SessionLocal, NiDB, Base
from sqlalchemy.orm import Session

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI()

CORE_BANKING_URL = "http://localhost:8000"

# Dépendance pour obtenir la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/process_transaction/", response_model=TransactionResponse)
async def process_transaction(request: TransactionRequest, db: Session = Depends(get_db)):
    # In a real system, we'd do some validation and routing logic here
    
    # For now, we'll just forward the request to the core banking service
    async with httpx.AsyncClient() as client:
        try:
            account_response = await client.get(f"{CORE_BANKING_URL}/accounts/card/{request.card_number}")
            print(account_response.status_code)
            if account_response.status_code !=200:
                # Persist successful response
                db_response = NiDB(
                    transaction_id=request.transaction_id,
                    card_number=request.card_number,
                    amount = request.amount,
                    atm_id=request.atm_id,
                    transaction_type = request.transaction_type,
                    status="failed",
                    message="Invalid Card number",
                    timestamp=datetime.now()
                )
                db.add(db_response)
                db.commit()
                return TransactionResponse(transaction_id=request.transaction_id,status="failed",message="Invalid Card number",timestamp=datetime.now())
            
            account = account_response.json()            
            
            response = await client.post(f"{CORE_BANKING_URL}/transactions/", json={
                "id": request.transaction_id,
                "account_id": account['id'],  # In a real system, we'd look up the account ID
                "amount": request.amount,
                "transaction_type": request.transaction_type
            })
            
            if response.status_code == 200:
                # Persist successful response
                db_response = NiDB(
                    transaction_id=request.transaction_id,
                    card_number=request.card_number,
                    amount = request.amount,
                    atm_id=request.atm_id,
                    transaction_type = request.transaction_type,
                    status="success",
                    message="Withdrawal successful",
                    timestamp=datetime.now()
                )
                db.add(db_response)
                db.commit()
                return TransactionResponse(
                    transaction_id=request.transaction_id,
                    status="success",
                    message="Transaction processed successfully",
                    timestamp=datetime.now()
                )
            else:
                # Persist failed response
                db_response = NiDB(
                    transaction_id=request.transaction_id,
                    card_number=request.card_number,
                    amount = request.amount,
                    atm_id=request.atm_id,
                    transaction_type = request.transaction_type,
                    status="failed",
                    message=f"Withdrawal failed: {response.json().get('detail', 'Unknown error')}",
                    timestamp=datetime.now()
                )
                db.add(db_response)
                db.commit()
                return TransactionResponse(
                    transaction_id=request.transaction_id,
                    status="failed",
                    message=f"Transaction failed: {response.json().get('detail', 'Unknown error')}",
                    timestamp=datetime.now()
                )
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error communicating with core banking: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}