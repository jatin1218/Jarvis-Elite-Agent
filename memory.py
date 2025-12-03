"""
Memory management for conversation history
"""
from datetime import datetime
from database import db  # Import from database.py, not define here


class MemoryAgent:
    """
    Agent for managing conversation memory
    """
    
    def save(self, query, response):
        """
        Save conversation to database
        """
        if not db:
            return
        
        try:
            db.table("conversation_log").insert({
                "query": query,
                "response": response,
                "timestamp": datetime.utcnow().isoformat()
            }).execute()
        except Exception as e:
            print(f"Error saving to memory: {e}")

    def recent(self, limit=4):
        """
        Retrieve recent conversations
        """
        if not db:
            return []
        
        try:
            res = db.table("conversation_log") \
                    .select("query,response") \
                    .order("id", desc=True) \
                    .limit(limit) \
                    .execute()
            
            return res.data if res.data else []
        
        except Exception as e:
            print(f"Error retrieving memory: {e}")
            return []