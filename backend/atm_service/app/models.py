from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime
from database import Base

class AtmDB(Base):
    __tablename__ = 'transaction'

    transaction_id = Column(String, primary_key=True)
    card_number = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    atm_id = Column(String, nullable=False)
    transaction_type = Column(String)
    timestamp = Column(DateTime, default=datetime.now)
    status = Column(String, nullable=False)
    message = Column(String, nullable=False)


class TransactionOut(BaseModel):
    transaction_id: str
    card_number : str
    transaction_type :str
    amount: float
    atm_id: str
    status: str
    message: str
    timestamp: datetime

    class Config:
        orm_mode = True


class WithdrawalRequest(BaseModel):
    card_number: str
    amount: float
    atm_id: str
    transaction_type: str

class WithdrawalResponse(BaseModel):
    transaction_id: str
    status: str
    message: str
    transaction_type: str
    timestamp: datetime = Field(default_factory=datetime.now)