from enum import Enum

class CustomerStatus(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class Customer:
    def __init__(self, customer_id, name, email, phone, address, status=CustomerStatus.ACTIVE):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.status = status
        self.accounts = []
        self.interaction_logs = []

    def add_account(self, account):
        self.accounts.append(account)

    def log_interaction(self, log):
        self.interaction_logs.append(log)

    def __repr__(self):
        return f"<Customer {self.customer_id} - {self.name}>"
