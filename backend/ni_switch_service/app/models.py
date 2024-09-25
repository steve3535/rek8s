from pydantic import BaseModel
from datetime import datetime
from database import Base
from sqlalchemy import Column, String, Float, DateTime

class NiDB(Base):
    __tablename__ = 'transaction'

    transaction_id = Column(String, primary_key=True)
    card_number = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    atm_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    status = Column(String, nullable=False)
    message = Column(String, nullable=False)
    transaction_type = Column(String, nullable=False)

class TransactionOut(BaseModel):
    transaction_id: str
    card_number : str
    amount: float
    atm_id: str
    status: str
    message: str
    transaction_type: str
    timestamp: datetime

    class Config:
        orm_mode = True


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
    transaction_type: str
    timestamp: datetime=datetime.now()

