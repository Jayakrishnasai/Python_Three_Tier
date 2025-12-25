import os
import logging
from typing import Optional, List, Dict, Any
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseTier:
    """
    Data Access Layer (DAL) for Supabase.
    Updated to handle Multi-User Isolation (user_id).
    """
    def __init__(self, client: Client):
        self.client = client

    @classmethod
    def create(cls) -> "DatabaseTier":
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")

        if not url or not key:
            logger.error("Supabase credentials missing.")
            raise RuntimeError("Supabase URL or Key missing.")

        try:
            client = create_client(url, key)
            return cls(client)
        except Exception as e:
            logger.error(f"Failed to connect to Supabase: {str(e)}")
            raise

    def is_working(self) -> bool:
        return self.client is not None

    def get_tasks(self, user_id: str):
        """Fetch tasks only for a specific user to ensure data isolation."""
        try:
            return self.client.table("tasks") \
                .select("*") \
                .eq("user_id", user_id) \
                .order("created_at") \
                .execute()
        except Exception as e:
            logger.error(f"Error fetching tasks for user {user_id}: {str(e)}")
            raise

    def add_task(self, user_id: str, task_data: dict):
        """Insert task and explicitly tie it to the user."""
        try:
            # Enforce user_id ownership
            task_data["user_id"] = user_id
            return self.client.table("tasks") \
                .insert(task_data) \
                .execute()
        except Exception as e:
            logger.error(f"Error adding task for user {user_id}: {str(e)}")
            raise

    def update_task(self, user_id: str, task_id: str, task_data: dict):
        """Update task ensuring the user owns it."""
        try:
            return self.client.table("tasks") \
                .update(task_data) \
                .eq("id", task_id) \
                .eq("user_id", user_id) \
                .execute()
        except Exception as e:
            logger.error(f"Error updating task {task_id} for user {user_id}: {str(e)}")
            raise

    def delete_task(self, user_id: str, task_id: str):
        """Delete task ensuring the user owns it."""
        try:
            return self.client.table("tasks") \
                .delete() \
                .eq("id", task_id) \
                .eq("user_id", user_id) \
                .execute()
        except Exception as e:
            logger.error(f"Error deleting task {task_id} for user {user_id}: {str(e)}")
            raise
