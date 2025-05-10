from enum import Enum

class Role(Enum):
    ADMIN = "Admin"
    MANAGER = "Manager"
    ANALYST = "Analyst"

class Staff:
    def __init__(self, staff_id, name, email, role=Role.MANAGER):
        self.staff_id = staff_id
        self.name = name
        self.email = email
        self.role = role
        self.logs = []

    def add_log(self, log):
        self.logs.append(log)

    def __repr__(self):
        return f"<Staff {self.staff_id} - {self.name} | {self.role.value}>"
