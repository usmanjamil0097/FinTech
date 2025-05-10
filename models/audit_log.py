from datetime import datetime

class AuditLog:
    def __init__(self, log_id, action, actor_id, target_id, description):
        self.log_id = log_id
        self.timestamp = datetime.now()
        self.action = action
        self.actor_id = actor_id
        self.target_id = target_id
        self.description = description

    def __repr__(self):
        return f"<AuditLog {self.log_id} | {self.timestamp} | {self.action} | Actor: {self.actor_id}>"
