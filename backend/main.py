from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import DatabaseTier

app = FastAPI(title="Three-Tier Python API Production")

# In a real production app, this would be extracted from a JWT token (OAuth2)
# For the current frontend demo, we use a consistent Mock ID to satisfy the 'user_id NOT NULL' constraint.
MOCK_USER_ID = "00000000-0000-0000-0000-000000000001"

def get_db():
    try:
        return DatabaseTier.create()
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

# Dependency to get the current user context
# This is where you would implement real Auth (e.g., Supabase Auth / JWT verification)
def get_current_user():
    return MOCK_USER_ID

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskSchema(BaseModel):
    title: str
    status: str = "pending"
    priority: str = "medium"

@app.get("/")
async def root(db: DatabaseTier = Depends(get_db)):
    return {
        "message": "Welcome to the Three-Tier Python API",
        "database_connected": db.is_working(),
        "user_context": "active"
    }

@app.get("/tasks")
async def get_tasks(
    db: DatabaseTier = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    try:
        response = db.get_tasks(user_id)
        return response.data
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch tasks.")

@app.post("/tasks")
async def create_task(
    task: TaskSchema, 
    db: DatabaseTier = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    try:
        response = db.add_task(user_id, task.dict())
        return response.data
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create task.")

@app.put("/tasks/{task_id}")
async def update_task(
    task_id: str, 
    task: TaskSchema, 
    db: DatabaseTier = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    try:
        response = db.update_task(user_id, task_id, task.dict())
        return response.data
    except Exception:
        raise HTTPException(status_code=500, detail=f"Failed to update task {task_id}.")

@app.delete("/tasks/{task_id}")
async def delete_task(
    task_id: str, 
    db: DatabaseTier = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    try:
        response = db.delete_task(user_id, task_id)
        return response.data
    except Exception:
        raise HTTPException(status_code=500, detail=f"Failed to delete task {task_id}.")
