from pydantic import BaseModel, Field
from datetime import datetime

class WithdrawalRequest(BaseModel):
    card_number: str
    amount: float
    atm_id: str
    timestamp: datetime = Field(default_factory=datetime.now)

class WithdrawalResponse(BaseModel):
    transaction_id: str
    status: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)