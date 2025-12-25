import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class DatabaseTier:
    def __init__(self):
        self.url: str = os.getenv("SUPABASE_URL", "")
        self.key: str = os.getenv("SUPABASE_KEY", "")
        self.client: Client = None
        
        if self.url and self.key:
            self.client = create_client(self.url, self.key)

    def is_working(self):
        return self.client is not None

    def get_tasks(self):
        if not self.client:
            return None
        return self.client.table("tasks").select("*").order("created_at").execute()

    def add_task(self, task_data: dict):
        if not self.client:
            return None
        return self.client.table("tasks").insert(task_data).execute()

    def update_task(self, task_id: str, task_data: dict):
        if not self.client:
            return None
        return self.client.table("tasks").update(task_data).eq("id", task_id).execute()

    def delete_task(self, task_id: str):
        if not self.client:
            return None
        return self.client.table("tasks").delete().eq("id", task_id).execute()

# Singleton instance
db = DatabaseTier()
