from pydantic import BaseModel
from datetime import datetime

class Account(BaseModel):
    id: int
    balance: float

class Transaction(BaseModel):
    id: int
    account_id: int
    amount: float
    transaction_type: str
    timestamp: datetime = datetime.now()