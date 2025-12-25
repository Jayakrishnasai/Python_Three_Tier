import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Three-Tier Python API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, specify the actual origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase Setup
url: str = os.getenv("SUPABASE_URL", "")
key: str = os.getenv("SUPABASE_KEY", "")

if not url or not key:
    print("Warning: SUPABASE_URL or SUPABASE_KEY not found in environment variables.")

supabase: Client = create_client(url, key) if url and key else None

class Task(BaseModel):
    title: str
    status: str = "pending"
    priority: str = "medium"

@app.get("/")
async def root():
    return {"message": "Welcome to the Three-Tier Python API", "status": "online"}

@app.get("/tasks")
async def get_tasks():
    if not supabase:
        return [{"id": 1, "title": "Setup Supabase :)", "status": "pending", "priority": "high"}]
    
    try:
        response = supabase.table("tasks").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tasks")
async def create_task(task: Task):
    if not supabase:
        raise HTTPException(status_code=503, detail="Database connection not configured")
    
    try:
        response = supabase.table("tasks").insert(task.dict()).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task: Task):
    if not supabase:
        raise HTTPException(status_code=503, detail="Database connection not configured")
    
    try:
        response = supabase.table("tasks").update(task.dict()).eq("id", task_id).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    if not supabase:
        raise HTTPException(status_code=503, detail="Database connection not configured")
    
    try:
        response = supabase.table("tasks").delete().eq("id", task_id).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
