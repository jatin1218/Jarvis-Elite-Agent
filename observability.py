"""
Observability and logging system
"""
from datetime import datetime
from database import db  # FIXED: Import from database.py, not memory.py


class Observability:
    """
    Observability and logging system
    """

    def log(self, agent, action, payload):
        """
        Log agent actions
        """
        if not db:
            print(f"[LOG] {agent}.{action}: {str(payload)[:100]}")
            return
        
        try:
            db.table("agent_logs").insert({
                "agent": agent,
                "action": action,
                "payload": str(payload),
                "timestamp": datetime.utcnow().isoformat()
            }).execute()
        except Exception as e:
            print(f"Logging error: {e}")

    def metric(self, name):
        """
        Record metrics
        """
        if not db:
            print(f"[METRIC] {name}")
            return
        
        try:
            db.table("metrics").insert({
                "metric": name,
                "timestamp": datetime.utcnow().isoformat()
            }).execute()
        except Exception as e:
            print(f"Metrics error: {e}")


obs = Observability()