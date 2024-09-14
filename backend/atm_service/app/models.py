from pydantic import BaseModel 
from datetime import datetime 

class WithdrawalRequest(BaseModel):
    card_number: str 
    amount: float 
    atm_id: str 
    timestamp: datetime=datetime.now()

class WithdrawalResponse(BaseModel):
    transaction_id: str 
    status: str 
    message: str 
    timestamp: datetime=datetime.now() 

    