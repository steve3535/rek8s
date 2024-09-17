from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
SQLALCHEMY_DATABASE_URL = "sqlite:///./atm.db"  # Vous pouvez changer cette URL pour une base de données différente.

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AtmDB(Base):
    __tablename__ = 'transaction'

    transaction_id = Column(String, primary_key=True)
    card_number = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    atm_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    status = Column(String, nullable=False)
    message = Column(String, nullable=False)
