from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database import Base


# SQLAlchemy Models (for persistence)
Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
 
    accounts = relationship("Account", back_populates="customer")


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Float, default=0)
    customer_id = Column(Integer, ForeignKey("customers.id"), unique=True, nullable=False)
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")
    customer = relationship("Customer", back_populates="accounts")
    cards = relationship("Card", back_populates="account")
    #transactions = relationship("Transaction", back_populates="account") 


class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String, unique=True, nullable=False, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    pin = Column(Integer, nullable=False)  
    account = relationship("Account", back_populates="cards")
    

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"))
    amount = Column(Float)
    transaction_type = Column(String)
    status = Column(String, nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)  # Ajout du champ timestamp


    account = relationship("Account", back_populates="transactions")  # Relation avec Account


# Pydantic Models (for validation and API interaction)

class AccountCreate(BaseModel):
    balance: float
    customer_id: int 

class AccountOut(BaseModel):
    id: int
    balance: float
    customer_id: int 
    class Config:
        orm_mode = True

class AccountUpdate(BaseModel):
    balance: float

class TransactionCreate(BaseModel):
    account_id: int
    amount: float
    transaction_type: str

class TransactionOut(BaseModel):
    id: int
    account_id: int
    amount: float
    transaction_type: str
    status: str
    message: str
    timestamp: datetime

    class Config:
        orm_mode = True


class CustomerCreate(BaseModel):
    name: str
    email: str

class CustomerOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

class  CustomerUpdate(BaseModel):
    name: str
    email: str

class CardCreate(BaseModel):
    card_number: str
    account_id: int
    pin: int

class CardOut(BaseModel):
    id: int
    card_number: str
    account_id: int

    class Config:
        orm_mode = True

class CardUpdate(BaseModel):
    pin: int