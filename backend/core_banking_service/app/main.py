from fastapi import FastAPI, HTTPException
from .models import Account, Transaction
from .database import accounts, transactions

app = FastAPI()

@app.post("/accounts")
@app.post("/accounts/")
async def create_account(account: Account):
    accounts[account.id] = account
    return account

@app.get("/accounts/{account_id}")
async def read_account(account_id: int):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    return accounts[account_id]

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