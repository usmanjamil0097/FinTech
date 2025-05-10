import unittest
from models.customer import Customer, CustomerStatus
from models.account import Account, AccountType

class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.customer = Customer(
            customer_id="1",
            name="Alice",
            email="alice@example.com",
            phone="1234567890",
            address="123 Street",
            status=CustomerStatus.ACTIVE
        )

    def test_customer_creation(self):
        self.assertEqual(self.customer.name, "Alice")
        self.assertEqual(self.customer.status, CustomerStatus.ACTIVE)

    def test_add_account(self):
        account = Account(account_number="A1", account_type=AccountType.SAVINGS)
        self.customer.add_account(account)
        self.assertEqual(len(self.customer.accounts), 1)
        self.assertEqual(self.customer.accounts[0].account_number, "A1")

    def test_log_interaction(self):
        self.customer.log_interaction("Called for KYC update")
        self.assertIn("Called for KYC update", self.customer.interaction_logs)

if __name__ == '__main__':
    unittest.main()
