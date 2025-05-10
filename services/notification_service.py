class NotificationService:
    def send_alert(self, recipient_email: str, message: str):
        print(f"[ALERT] Sent to {recipient_email}: {message}")

    def send_transaction_alert(self, customer, tx):
        if tx.status.name == "FRAUDULENT":
            self.send_alert(customer.email, f"⚠️ Suspicious transaction detected: {tx}")
