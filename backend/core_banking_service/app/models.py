from pydantic import BaseModel
from datetime import datetime

class Account(BaseModel):
    id: int
    balance: float

class Transaction(BaseModel):
    id: str
    account_id: int
    amount: float
    transaction_type: str
    timestamp: datetime = datetime.now()

class Customer(BaseModel):
    id: int
    name: str
    email: str 

class Card(BaseModel):
    id: int
    card_number: str  
    account_id: int 
    pin: int     