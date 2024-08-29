from datetime import datetime

TXN_CREDIT = 201
TXN_DEBIT = 101

class Customer:
    def __init__(self, customer_id, name, address, phone):
        self.customer_id = customer_id
        self.name = name
        self.address = address
        self.phone = phone
        self.accounts = []  # List to hold Account objects

    def add_account(self, account):
        if account not in self.accounts:
          self.accounts.append(account)
          account.customer = self 

    def get_accounts(self):
        return self.accounts


class Account:
    def __init__(self, account_number, account_type, customer, initial_balance=0):
        self.account_number = account_number
        self.account_type = account_type
        self.customer = customer
        self.balance = initial_balance
        self.cards = []  # List to hold Card objects

    def add_card(self, card):
        if card not in self.cards:        
          self.cards.append(card)
          card.account = self 

    def get_cards(self):
        return self.cards

    def update_balance(self, txn_code ,amount):
        if txn_code == TXN_CREDIT:
          self.balance += amount
        elif txn_code == TXN_DEBIT:
          self.balance -= amount

    def get_balance(self):
        return self.balance

class Card:
    CARD_TYPES = ['ORA', 'VISA', 'UEMOA']

    def __init__(self, card_number, card_type, account, expiry_date):
        if card_type not in self.CARD_TYPES:
            raise ValueError(f"Invalid card type. Must be one of {self.CARD_TYPES}")
        
        self.card_number = card_number
        self.card_type = card_type
        self.account = account
        self.expiry_date = expiry_date
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def activate(self):
        self.is_active = True

    def is_valid(self):
        return self.is_active and self.expiry_date > datetime.now().date()