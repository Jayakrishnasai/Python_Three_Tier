# Production-ready Python Dockerfile
FROM python:3.11-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies (including curl for healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create a non‑root user before copying code (so files are owned correctly)
RUN adduser --disabled-password --gecos "" appuser

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (now owned by appuser)
COPY . .
RUN chown -R appuser /app

# Switch to non‑root user
USER appuser

# Expose the FastAPI port
EXPOSE 8000

# Entrypoint runs DB init then starts Gunicorn
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
