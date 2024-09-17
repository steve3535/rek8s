from fastapi import FastAPI, HTTPException
from models import TransactionRequest, TransactionResponse
import httpx
from datetime import datetime

app = FastAPI()

CORE_BANKING_URL = "http://localhost:8000"

@app.post("/process_transaction/", response_model=TransactionResponse)
async def process_transaction(request: TransactionRequest):
    # In a real system, we'd do some validation and routing logic here
    
    # For now, we'll just forward the request to the core banking service
    async with httpx.AsyncClient() as client:
        try:
            account_response = await client.get(f"{CORE_BANKING_URL}/accounts/card/{request.card_number}")
            print(account_response.status_code)
            if account_response.status_code !=200:
                return TransactionResponse(transaction_id=request.transaction_id,status="failed",message="Invalid Card number",timestamp=datetime.now())
            
            account = account_response.json()            
            
            response = await client.post(f"{CORE_BANKING_URL}/transactions/", json={
                "id": request.transaction_id,
                "account_id": account['id'],  # In a real system, we'd look up the account ID
                "amount": request.amount,
                "transaction_type": request.transaction_type
            })
            
            if response.status_code == 200:
                return TransactionResponse(
                    transaction_id=request.transaction_id,
                    status="success",
                    message="Transaction processed successfully",
                    timestamp=datetime.now()
                )
            else:
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