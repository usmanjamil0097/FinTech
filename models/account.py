from enum import Enum

class AccountType(Enum):
    SAVINGS = "Savings"
    CURRENT = "Current"
    LOAN = "Loan"

class Account:
    def __init__(self, account_number, account_type, balance=0.0):
        self.account_number = account_number
        self.account_type = account_type
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def __repr__(self):
        return f"<Account {self.account_number} | {self.account_type.value} | Balance: {self.balance:.2f}>"
