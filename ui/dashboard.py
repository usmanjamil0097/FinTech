import tkinter as tk
from tkinter import messagebox
from models.customer import Customer
from models.account import Account, AccountType
from services.transaction_service import TransactionService, TransactionType
from services.analytics_service import AnalyticsService
from utils.database import Database

class FinSecureApp:
    def __init__(self, root, db):
        self.root = root
        self.root.title("FinSecure - Manager Dashboard")
        self.root.geometry("500x450")
        self.root.configure(padx=20, pady=20)

        self.db = db
        self.transactions_db = Database("data/transactions.json")
        self.transactions_db.load()

        self.customers = self.load_customers()
        self.transaction_service = TransactionService(self.transactions_db)  # ✅ pass DB here
        self.analytics_service = AnalyticsService()

        self.build_ui()

    def build_ui(self):
        self.root.configure(bg="#e8f0fe")  # Soft blue background

        header = tk.Label(
            self.root, text="📊 FinSecure Dashboard",
            font=("Helvetica", 20, "bold"), fg="#0b5394", bg="#e8f0fe"
        )
        header.pack(pady=(0, 20))

        btn_frame = tk.Frame(self.root, bg="#e8f0fe")
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame, text="➕ Add Customer", width=20,
            bg="#4a90e2", fg="white", font=("Helvetica", 10, "bold"),
            command=self.add_customer_popup
        ).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(
            btn_frame, text="📈 Show Insights", width=20,
            bg="#007acc", fg="white", font=("Helvetica", 10, "bold"),
            command=self.show_insights
        ).grid(row=0, column=1, padx=5, pady=5)

        label = tk.Label(self.root, text="👥 Customers", font=("Helvetica", 12, "bold"),
                        fg="#1a237e", bg="#e8f0fe")
        label.pack(anchor='w', padx=5)

        listbox_frame = tk.Frame(self.root, bg="#e8f0fe", bd=2, relief="groove")
        listbox_frame.pack(pady=10, padx=5)

        self.customer_listbox = tk.Listbox(
            listbox_frame, width=50, height=10,
            font=("Helvetica", 10), fg="#0d47a1", bg="white", selectbackground="#bbdefb"
        )
        self.customer_listbox.pack(padx=5, pady=5)

        for customer in self.customers:
            self.customer_listbox.insert(tk.END, f"{customer.name} ({customer.customer_id})")

        tk.Button(
            self.root, text="🔍 View Accounts", width=30,
            bg="#1976d2", fg="white", font=("Helvetica", 10, "bold"),
            command=self.view_accounts_popup
        ).pack(pady=10)

    def load_customers(self):
        customer_dicts = self.db.get("customers")
        customers = []
        for c in customer_dicts:
            customer = Customer(
                customer_id=c["customer_id"],
                name=c["name"],
                email=c["email"],
                phone=c["phone"],
                address=c["address"]
            )
            print(customer)
            # Recreate account object
            for a in c.get("accounts", []):
                account = Account(
                    account_number=a["account_number"],
                    account_type=AccountType[a["account_type"]],
                    balance=a["balance"]
                )
                customer.add_account(account)
            customer.interaction_logs = c.get("interaction_logs", [])
            customers.append(customer)
        return customers

    def save_customers(self):
        serialized = []
        for c in self.customers:
            serialized.append({
                "customer_id": c.customer_id,
                "name": c.name,
                "email": c.email,
                "phone": c.phone,
                "address": c.address,
                "status": c.status.name,
                "interaction_logs": c.interaction_logs,
                "accounts": [
                    {
                        "account_number": a.account_number,
                        "account_type": a.account_type.name,
                        "balance": a.balance
                    } for a in c.accounts
                ]
            })
        self.db.set("customers", serialized)

    def add_customer_popup(self):
        popup = tk.Toplevel()
        popup.title("Add Customer")
        popup.geometry("350x250")
        popup.configure(padx=20, pady=20)

        fields = ["Name", "Email", "Phone", "Address"]
        entries = {}

        for i, field in enumerate(fields):
            tk.Label(popup, text=field + ":", font=("Helvetica", 10)).grid(row=i, column=0, sticky='w', pady=5)
            entry = tk.Entry(popup, width=30)
            entry.grid(row=i, column=1, pady=5)
            entries[field.lower()] = entry

        def submit():
            customer = Customer(
                customer_id=str(len(self.customers)+1),
                name=entries["name"].get(),
                email=entries["email"].get(),
                phone=entries["phone"].get(),
                address=entries["address"].get()
            )
            account = Account(account_number=f"ACC{customer.customer_id}", account_type=AccountType.SAVINGS)
            customer.add_account(account)
            self.customers.append(customer)
            self.customer_listbox.insert(tk.END, f"{customer.name} ({customer.customer_id})")
            
            self.save_customers()  # ✅ Save immediately
            
            popup.destroy()

        tk.Button(popup, text="✅ Submit", command=submit).grid(row=4, columnspan=2, pady=15)

    def view_accounts_popup(self):
        selected = self.customer_listbox.curselection()
        if not selected:
            messagebox.showwarning("Select Customer", "Please select a customer.")
            return

        index = selected[0]
        customer = self.customers[index]

        popup = tk.Toplevel()
        popup.title(f"{customer.name} - Account Details")
        popup.geometry("400x250")
        popup.configure(padx=20, pady=20)

        if not customer.accounts:
            tk.Label(popup, text="No accounts available").pack()
            return

        account = customer.accounts[0]
        tk.Label(popup, text=f"🏦 Account: {account.account_number}", font=("Helvetica", 12, "bold")).pack(anchor='w', pady=5)
        balance_label = tk.Label(popup, text=f"💰 Balance: {account.balance:.2f}", font=("Helvetica", 11))
        balance_label.pack(anchor='w', pady=5)

        amount_frame = tk.Frame(popup)
        amount_frame.pack(pady=10)

        tk.Label(amount_frame, text="Enter Amount:", font=("Helvetica", 10)).grid(row=0, column=0, padx=5)
        amount_entry = tk.Entry(amount_frame, width=15)
        amount_entry.grid(row=0, column=1)

        def deposit():
            amount_str = amount_entry.get()
            if not amount_str.strip():
                messagebox.showerror("Input Error", "Please enter an amount.")
                return
            try:
                amount = float(amount_str)
                tx = self.transaction_service.perform_transaction(account, TransactionType.DEPOSIT, amount)
                balance_label.config(text=f"💰 Balance: {account.balance:.2f}")
                messagebox.showinfo("Success", f"Deposited: {amount}")
            except ValueError:
                messagebox.showerror("Input Error", "Invalid number entered.")

        def withdraw():
            amount_str = amount_entry.get()
            if not amount_str.strip():
                messagebox.showerror("Input Error", "Please enter an amount.")
                return
            try:
                amount = float(amount_str)
                tx = self.transaction_service.perform_transaction(account, TransactionType.WITHDRAWAL, amount)
                balance_label.config(text=f"💰 Balance: {account.balance:.2f}")
                if tx.status.name == "FAILED":
                    messagebox.showwarning("Failed", "Insufficient balance.")
                else:
                    messagebox.showinfo("Success", f"Withdrawn: {amount}")
            except ValueError:
                messagebox.showerror("Input Error", "Invalid number entered.")

        btn_frame = tk.Frame(popup)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="➕ Deposit", width=12, command=deposit).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="➖ Withdraw", width=12, command=withdraw).grid(row=0, column=1, padx=10)

    def show_insights(self):
        insights = self.analytics_service.get_customer_insights(self.customers)
        messagebox.showinfo(
            "Customer Insights",
            f"👥 Total Customers: {insights['total_customers']}\n✅ Active: {insights['active_customers']}\n📉 Churn Rate: {insights['churn_rate']}%"
        )


