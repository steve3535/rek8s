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