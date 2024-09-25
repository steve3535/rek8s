from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import AccountCreate, AccountOut, TransactionCreate, TransactionOut, CustomerCreate, CustomerOut, CardCreate, CardOut
from models import Account, Transaction, Customer, Card, CardUpdate,  Base, CustomerUpdate, AccountUpdate
from datetime import datetime
from database import engine, get_db
from typing import List
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()



# Définir les origines autorisées (peut-être '*' pour autoriser toutes les origines)
origins = [
    "http://127.0.0.1:5500",  # Origine pour votre frontend
    "http://localhost:5500",  # Autre origine potentielle
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






# Create a new customer
@app.post("/customers/", response_model=CustomerOut)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = Customer(name=customer.name, email=customer.email)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.get("/customers/", response_model=List[CustomerOut])
def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Customer).offset(skip).limit(limit).all()

@app.get("/customers/{customer_id}", response_model=CustomerOut)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.put("/customers/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db_customer.name = customer.name
    db_customer.email = customer.email
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.delete("/customers/{customer_id}", response_model=CustomerOut)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(db_customer)
    db.commit()
    return db_customer

# Create a new account with customer_id
@app.post("/accounts/", response_model=AccountOut)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == account.customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db_account = Account(balance=account.balance, customer_id=account.customer_id)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@app.get("/accounts/", response_model=List[AccountOut])
def get_all_accounts(db: Session = Depends(get_db)):
    accounts = db.query(Account).all()
    return accounts


@app.get("/accounts/{account_id}", response_model=AccountOut)
def read_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@app.put("/accounts/{account_id}", response_model=AccountOut)
def update_account(account_id: int, account: AccountUpdate, db: Session = Depends(get_db)):
    db_account = db.query(Account).filter(Account.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    db_account.balance = account.balance
    db.commit()
    db.refresh(db_account)
    return db_account

@app.delete("/accounts/{account_id}", response_model=AccountOut)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    db_account = db.query(Account).filter(Account.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    db.delete(db_account)
    db.commit()
    return db_account



# Create a new card
@app.post("/cards/", response_model=CardOut)
def create_card(card: CardCreate, db: Session = Depends(get_db)):
    db_card = Card(card_number=card.card_number, account_id=card.account_id, pin=card.pin)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


@app.get("/cards/", response_model=List[CardOut])
def read_cards(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Card).offset(skip).limit(limit).all()

@app.get("/cards/{card_id}", response_model=CardOut)
def read_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

@app.put("/cards/{card_id}", response_model=CardOut)
def update_card(card_id: int, card: CardUpdate, db: Session = Depends(get_db)):
    db_card = db.query(Card).filter(Card.id == card_id).first()
    if not db_card:
        raise HTTPException(status_code=404, detail="Card not found")
    db_card.pin = card.pin
    db.commit()
    db.refresh(db_card)
    return db_card

@app.delete("/cards/{card_id}", response_model=CardOut)
def delete_card(card_id: int, db: Session = Depends(get_db)):
    db_card = db.query(Card).filter(Card.id == card_id).first()
    if not db_card:
        raise HTTPException(status_code=404, detail="Card not found")
    db.delete(db_card)
    db.commit()
    return db_card

# Get account details using card number
@app.get("/accounts/card/{card_number}", response_model=AccountOut)
def get_account_from_card(card_number: str, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.card_number == card_number).first()
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    account = db.query(Account).filter(Account.id == card.account_id).first()
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

# Create a new transaction
@app.post("/transactions/", response_model=TransactionOut)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == transaction.account_id).first()
    #db_transaction = None
    if account is None:
        # Enregistrer la transaction échouée avec un message
        db_transaction = Transaction(
            account_id=transaction.account_id,
            amount=transaction.amount,
            status="failed",
            message="Account not found",
            transaction_type=transaction.transaction_type,
            timestamp=datetime.utcnow()
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction

    if transaction.transaction_type == "withdrawal":
        if account.balance < transaction.amount:
            # Enregistrer la transaction échouée pour fonds insuffisants
            db_transaction = Transaction(
                account_id=transaction.account_id,
                amount=transaction.amount,
                status="failed",
                message="Insufficient funds",
                transaction_type=transaction.transaction_type,
                timestamp=datetime.utcnow()
            )
            db.add(db_transaction)
            db.commit()
            db.refresh(db_transaction)
            return db_transaction

        # Mise à jour du solde en cas de retrait
        account.balance -= transaction.amount

    elif transaction.transaction_type == "deposit":
        # Mise à jour du solde en cas de dépôt
        
        account.balance += transaction.amount
        #return db_transaction

    else:
        # Enregistrer la transaction échouée en cas de type de transaction invalide
        db_transaction = Transaction(
            account_id=transaction.account_id,
            amount=transaction.amount,
            status="failed",
            message="Invalid transaction type",
            transaction_type=transaction.transaction_type,
            timestamp=datetime.utcnow()
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction

    # Enregistrer la transaction réussie
    db_transaction = Transaction(
        account_id=transaction.account_id,
        amount=transaction.amount,
        status="success",
        message="Transaction successful",
        transaction_type=transaction.transaction_type,
        timestamp=datetime.utcnow()
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction


@app.get("/transactions/", response_model=List[TransactionOut])
def get_transaction(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).order_by(Transaction.timestamp.desc()).offset(skip).limit(limit).all()
    return transactions