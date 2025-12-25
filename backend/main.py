from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import DatabaseTier

app = FastAPI(title="Three-Tier Python API Production")

# Dependency to get DatabaseTier instance
def get_db():
    try:
        return DatabaseTier.create()
    except RuntimeError as e:
        # If DB is not configured, we catch it here
        # In a real prod app, you might want to return a dummy or fail fast
        raise HTTPException(status_code=503, detail=str(e))

# Enable CORS for frontend
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
        "database_connected": db.is_working()
    }

@app.get("/tasks")
async def get_tasks(db: DatabaseTier = Depends(get_db)):
    try:
        response = db.get_tasks()
        return response.data
    except Exception as e:
        # Errors are already logged in DatabaseTier
        raise HTTPException(status_code=500, detail="Failed to fetch tasks from database.")

@app.post("/tasks")
async def create_task(task: TaskSchema, db: DatabaseTier = Depends(get_db)):
    try:
        response = db.add_task(task.dict())
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create task.")

@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task: TaskSchema, db: DatabaseTier = Depends(get_db)):
    try:
        response = db.update_task(task_id, task.dict())
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update task {task_id}.")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str, db: DatabaseTier = Depends(get_db)):
    try:
        response = db.delete_task(task_id)
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete task {task_id}.")
