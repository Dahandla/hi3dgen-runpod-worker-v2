FROM python:3.10-slim

# -----------------------------------------------------------------------------
# Environment
# -----------------------------------------------------------------------------

ENV PYTHONUNBUFFERED=1 \
    HF_HOME=/models/hf \
    TORCH_HOME=/models/torch \
    TRANSFORMERS_CACHE=/models/hf

WORKDIR /app

# -----------------------------------------------------------------------------
# System dependencies
# -----------------------------------------------------------------------------

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libgl1 \
    libglib2.0-0 \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------------------------
# Create model directories
# -----------------------------------------------------------------------------

RUN mkdir -p /models/hf /models/torch /models/hi3dgen

# -----------------------------------------------------------------------------
# Python dependencies
# -----------------------------------------------------------------------------

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------------------------------------------------------
# Copy Hi3DGen Python code
# -----------------------------------------------------------------------------

COPY hi3dgen/ ./hi3dgen/

# -----------------------------------------------------------------------------
# Copy Hi3DGen model weights (downloaded into hi3dgen/ subdirectories)
# Models should be downloaded using download_models.py first
# The download script places models in: hi3dgen/trellis-normal-v0-1/, hi3dgen/yoso-normal-v1-8-1/, hi3dgen/BiRefNet/
COPY hi3dgen/trellis-normal-v0-1/ /models/hi3dgen/trellis-normal-v0-1/
COPY hi3dgen/yoso-normal-v1-8-1/ /models/hi3dgen/yoso-normal-v1-8-1/
COPY hi3dgen/BiRefNet/ /models/hi3dgen/BiRefNet/
# 
# Expected structure after download:
# Hi3DGen/
#   ├── pipeline.json
#   ├── models/
#   │   ├── sparse_structure_flow_model/
#   │   │   ├── sparse_structure_flow_model.json
#   │   │   └── sparse_structure_flow_model.safetensors
#   │   ├── sparse_structure_decoder/
#   │   │   ├── sparse_structure_decoder.json
#   │   │   └── sparse_structure_decoder.safetensors
#   │   ├── slat_flow_model/
#   │   │   ├── slat_flow_model.json
#   │   │   └── slat_flow_model.safetensors
#   │   └── slat_decoder_mesh/
#   │       ├── slat_decoder_mesh.json
#   │       └── slat_decoder_mesh.safetensors
#   └── ...

# -----------------------------------------------------------------------------
# Copy worker code
# -----------------------------------------------------------------------------

COPY handler.py .

# -----------------------------------------------------------------------------
# RunPod serverless entry
# -----------------------------------------------------------------------------

CMD ["python", "handler.py"]
