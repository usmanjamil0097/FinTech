from models.audit_log import AuditLog
import uuid

class ComplianceService:
    def __init__(self):
        self.audit_logs = []

    def log_action(self, actor_id, target_id, action, description):
        log = AuditLog(
            log_id=str(uuid.uuid4()),
            actor_id=actor_id,
            target_id=target_id,
            action=action,
            description=description
        )
        self.audit_logs.append(log)
        return log

    def get_logs(self):
        return self.audit_logs
