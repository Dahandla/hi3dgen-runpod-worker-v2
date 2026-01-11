FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Create model cache directories
RUN mkdir -p /models/hf /models/torch

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy handler and hi3dgen code
COPY handler.py .
COPY hi3dgen/ ./hi3dgen/

# RunPod serverless imports handler() function directly
CMD ["python", "handler.py"]
