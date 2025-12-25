import os
import logging
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseTier:
    """
    Data Access Layer (DAL) for Supabase.
    Isolates database logic from API routes for better testability and maintainability.
    """
    def __init__(self, client: Client):
        self.client = client

    @classmethod
    def create(cls) -> "DatabaseTier":
        """
        Factory method to create a DatabaseTier instance.
        Ensures credentials exist before trying to connect.
        """
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")

        if not url or not key:
            logger.error("Supabase credentials missing in environment variables.")
            raise RuntimeError("CRITICAL: Supabase URL or Key missing.")

        try:
            client = create_client(url, key)
            return cls(client)
        except Exception as e:
            logger.error(f"Failed to connect to Supabase: {str(e)}")
            raise

    def is_working(self) -> bool:
        """Check if the client is initialized."""
        return self.client is not None

    def get_tasks(self):
        try:
            return self.client.table("tasks") \
                .select("*") \
                .order("created_at") \
                .execute()
        except Exception as e:
            logger.error(f"Error fetching tasks: {str(e)}")
            raise

    def add_task(self, task_data: dict):
        try:
            return self.client.table("tasks") \
                .insert(task_data) \
                .execute()
        except Exception as e:
            logger.error(f"Error adding task: {str(e)}")
            raise

    def update_task(self, task_id: str, task_data: dict):
        try:
            return self.client.table("tasks") \
                .update(task_data) \
                .eq("id", task_id) \
                .execute()
        except Exception as e:
            logger.error(f"Error updating task {task_id}: {str(e)}")
            raise

    def delete_task(self, task_id: str):
        try:
            return self.client.table("tasks") \
                .delete() \
                .eq("id", task_id) \
                .execute()
        except Exception as e:
            logger.error(f"Error deleting task {task_id}: {str(e)}")
            raise
