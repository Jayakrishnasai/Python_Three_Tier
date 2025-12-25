from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import db

app = FastAPI(title="Three-Tier Python API")

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
async def root():
    return {
        "message": "Welcome to the Three-Tier Python API",
        "database_connected": db.is_working()
    }

@app.get("/tasks")
async def get_tasks():
    if not db.is_working():
        # Fallback/Mock data if DB is not configured
        return [{"id": "mock", "title": "Please configure SUPABASE_URL in .env", "status": "pending", "priority": "high"}]
    
    try:
        response = db.get_tasks()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tasks")
async def create_task(task: TaskSchema):
    if not db.is_working():
        raise HTTPException(status_code=503, detail="Database connection not configured")
    
    try:
        response = db.add_task(task.dict())
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task: TaskSchema):
    if not db.is_working():
        raise HTTPException(status_code=503, detail="Database connection not configured")
    
    try:
        response = db.update_task(task_id, task.dict())
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    if not db.is_working():
        raise HTTPException(status_code=503, detail="Database connection not configured")
    
    try:
        response = db.delete_task(task_id)
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
