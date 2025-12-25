#!/usr/bin/env bash
set -e

# Initialize the database schema if it doesn't exist
if [ -f "./init_db.py" ]; then
  python -m init_db
fi

# Start the FastAPI app with Gunicorn
exec gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
