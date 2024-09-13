from fastapi import FastAPI,HTTPException 
from .models import WithdrawalRequest,WithdrawalResponse 
from datetime import datetime
import uuid 
import httpx 

SWITCH_URL="http://127.0.0.1:8002"

app = FastAPI()

@app.post('/withdraw',response_model=WithdrawalResponse)
async def withdraw(request: WithdrawalRequest):
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
                return WithdrawalResponse(
                    transaction_id=transaction_id,
                    status="success",
                    message="Withdrawal successful",
                    timestamp=datetime.now()
                )
            else:
                return WithdrawalResponse(
                    transaction_id=transaction_id,
                    status="failed",
                    message=f"Withdrawal failed: {response.json().get('detail', 'Unknown error')}",
                    timestamp=datetime.now()
                )
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error communicating with switch: {str(e)}")    
        
@app.get('/health')        
async def health_check():
    return {"status": "healthy"}
