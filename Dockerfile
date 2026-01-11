FROM python:3.10-slim

WORKDIR /app

<<<<<<< HEAD
# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy handler
COPY handler.py .

# RunPod serverless imports handler() function directly
CMD ["python", "handler.py"]
=======
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY handler.py .

CMD ["python", "handler.py"]


# rebuild trigger
# rebuild trigger 2c

>>>>>>> 22b166206e16b761343add9d580dbfd18d339e66
