import unittest
from models.account import Account, AccountType
from models.transaction import TransactionType, TransactionStatus
from services.transaction_service import TransactionService

class TestTransaction(unittest.TestCase):

    def setUp(self):
        self.account = Account(account_number="T1", account_type=AccountType.SAVINGS, balance=1000.0)
        self.service = TransactionService()

    def test_deposit(self):
        tx = self.service.perform_transaction(self.account, TransactionType.DEPOSIT, 500.0)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertEqual(tx.status, TransactionStatus.SUCCESS)

    def test_withdrawal_success(self):
        tx = self.service.perform_transaction(self.account, TransactionType.WITHDRAWAL, 300.0)
        self.assertEqual(self.account.balance, 700.0)
        self.assertEqual(tx.status, TransactionStatus.SUCCESS)

    def test_withdrawal_insufficient_funds(self):
        tx = self.service.perform_transaction(self.account, TransactionType.WITHDRAWAL, 1500.0)
        self.assertEqual(tx.status, TransactionStatus.FAILED)

    def test_fraud_detection(self):
        tx = self.service.perform_transaction(self.account, TransactionType.DEPOSIT, 20000.0)
        is_fraud = self.service.detect_fraud(tx)
        self.assertTrue(is_fraud)
        self.assertEqual(tx.status, TransactionStatus.FRAUDULENT)

if __name__ == '__main__':
    unittest.main()
