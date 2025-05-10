from models.transaction import Transaction, TransactionType, TransactionStatus
from models.account import Account
import uuid
from datetime import datetime

class TransactionService:
    def __init__(self, db=None):  
        self.transaction_log = []
        self.db = db

    def perform_transaction(self, account: Account, trans_type: TransactionType, amount: float) -> Transaction:
        try:
            if trans_type == TransactionType.DEPOSIT:
                account.deposit(amount)
            elif trans_type == TransactionType.WITHDRAWAL:
                account.withdraw(amount)
            else:
                raise ValueError("Unsupported transaction type")
            status = TransactionStatus.SUCCESS
        except Exception:
            status = TransactionStatus.FAILED

        tx = Transaction(
            transaction_id=str(uuid.uuid4()),
            account_number=account.account_number,
            trans_type=trans_type,
            amount=amount,
            status=status
        )
        account.add_transaction(tx)
        self.transaction_log.append(tx)

        # ✅ Save to transactions.json
        if self.db:
            txs = self.db.get("transactions")
            txs.append({
                "transaction_id": tx.transaction_id,
                "account_number": tx.account_number,
                "trans_type": tx.trans_type.name,
                "amount": tx.amount,
                "timestamp": tx.timestamp.isoformat(),
                "status": tx.status.name
            })
            self.db.set("transactions", txs)

        return tx

    def detect_fraud(self, tx: Transaction) -> bool:
        if tx.amount > 10000:
            tx.status = TransactionStatus.FRAUDULENT
            return True
        return False
