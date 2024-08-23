from datetime import datetime 
TXN_WITHDRAWAL = '100'
TXN_DEPOSIT = '200'
TXN_REPLENISH = '300'

class Transaction():
    def __init__(self,txn_id,txn_code,txn_amount,card_number=None):
        self.txn_id = txn_id
        self.txn_code = txn_code
        self.txn_amount = txn_amount
        self.txn_date = datetime.now()
        self.card_number = card_number

class Journal():
    def __init__(self):
        self.transactions = []

    def add_transaction(self,txn):
        self.transactions.append(txn)

    def get_transactions(self):
        return self.transactions

class ATM():
    def __init__(self,id,name,location,agency_code,account_number,initial_balance):  
        self.id = id 
        self.name = name
        self.location = location
        self.agency_code = agency_code
        self.account_number = account_number
        self._balance = initial_balance
        self.journal = Journal()

    def process_transaction(self,transaction):
        self.journal.add_transaction(transaction)
        if transaction.txn_code == TXN_WITHDRAWAL: #withdraw
            self._balance -= transaction.txn_amount
        elif transaction.txn_code in [TXN_DEPOSIT,TXN_REPLENISH]: #deposit and replenish 
            self._balance += transaction.txn_amount
    
    def get_balance(self):
        return self._balance 

    def get_transactions(self):
        return self.journal.get_transactions()
    

