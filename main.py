from tkinter import Tk
from ui.dashboard import FinSecureApp
from utils.database import Database

db = Database("data/customers.json")
db.load()

def on_close(app):
    app.save_customers()
    app.root.destroy()

if __name__ == "__main__":
    root = Tk()
    app = FinSecureApp(root, db)
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(app))
    root.mainloop()
