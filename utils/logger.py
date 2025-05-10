from datetime import datetime

class Logger:
    def __init__(self, logfile="log.txt"):
        self.logfile = logfile

    def log(self, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        with open(self.logfile, "a") as f:
            f.write(log_entry + "\n")
        print(log_entry)  # Optional: also show on console
