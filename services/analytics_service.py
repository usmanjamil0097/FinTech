from models.customer import Customer
from models.transaction import TransactionStatus

class AnalyticsService:
    def get_customer_insights(self, customers: list[Customer]) -> dict:
        total_customers = len(customers)
        active_customers = sum(1 for c in customers if c.status.name == "ACTIVE")
        return {
            "total_customers": total_customers,
            "active_customers": active_customers,
            "churn_rate": round((1 - active_customers / total_customers) * 100, 2) if total_customers else 0
        }

    def get_transaction_summary(self, transactions: list) -> dict:
        total = len(transactions)
        frauds = sum(1 for t in transactions if t.status == TransactionStatus.FRAUDULENT)
        success = sum(1 for t in transactions if t.status == TransactionStatus.SUCCESS)
        return {
            "total_transactions": total,
            "fraudulent": frauds,
            "success_rate": round(success / total * 100, 2) if total else 0
        }
