from enum import Enum
from datetime import datetime

class TransactionType(Enum):
    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"
    TRANSFER = "Transfer"

class TransactionStatus(Enum):
    SUCCESS = "Success"
    FAILED = "Failed"
    FRAUDULENT = "Fraudulent"

class Transaction:
    def __init__(self, transaction_id, account_number, trans_type, amount, status=TransactionStatus.SUCCESS):
        self.transaction_id = transaction_id
        self.account_number = account_number
        self.trans_type = trans_type
        self.amount = amount
        self.timestamp = datetime.now()
        self.status = status

    def __repr__(self):
        return f"<Transaction {self.transaction_id} | {self.trans_type.value} | {self.amount} | {self.status.value}>"
