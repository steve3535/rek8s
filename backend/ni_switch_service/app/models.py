from pydantic import BaseModel
from datetime import datetime

class TransactionRequest(BaseModel):
    transaction_id: str
    card_number: str
    amount: float
    atm_id: str
    transaction_type: str

class TransactionResponse(BaseModel):
    transaction_id: str
    status: str
    message: str
    timestamp: datetime=datetime.now()

