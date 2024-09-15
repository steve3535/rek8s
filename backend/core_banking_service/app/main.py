from fastapi import FastAPI, HTTPException
from .models import Account, Transaction, Customer, Card 
from .database import accounts, transactions, customers, cards

app = FastAPI()

@app.post("/customers/")
async def create_customer(customer: Customer):
    customers[customer.id] = customer 
    return customer

@app.post("/accounts/")
async def create_account(account: Account):
    accounts[account.id] = account
    return account

@app.post("/cards/")
async def create_card(card: Card):
    cards[card.card_number] = card 
    return card

@app.get("/accounts/{account_id}")
async def read_account(account_id: int):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    return accounts[account_id]

@app.get("/accounts/card/{card_number}")
async def get_account_from_card(card_number:str):
    card = cards.get(card_number)
    if not(card):
        raise HTTPException(status_code=404,detail="CARD NOT FOUND")
    account=accounts.get(card.account_id)
    if not account:
        raise HTTPException(status_code=404,detail="ACCOUNT NOT FOUND")
    return account 

@app.post("/transactions/")
async def create_transaction(transaction: Transaction):
    if transaction.account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    account = accounts[transaction.account_id]
    if transaction.transaction_type == "withdrawal":
        if account.balance < transaction.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        account.balance -= transaction.amount
    elif transaction.transaction_type == "deposit":
        account.balance += transaction.amount
    transactions.append(transaction)
    return transaction

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
