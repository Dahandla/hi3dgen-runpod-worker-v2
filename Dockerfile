FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/models/hf
ENV TORCH_HOME=/models/torch
ENV TRANSFORMERS_CACHE=/models/hf

WORKDIR /app

# -----------------------------------------------------------------------------
# System dependencies
# -----------------------------------------------------------------------------

RUN apt-get update && apt-get install -y \
    build-essential \
    python3 \
    python3-pip \
    git \
    libgl1 \
    libglib2.0-0 \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

# -----------------------------------------------------------------------------
# Create model directories
# -----------------------------------------------------------------------------

RUN mkdir -p /models/hf /models/torch /models/hi3dgen

# -----------------------------------------------------------------------------
# Python dependencies (CUDA torch!)
# -----------------------------------------------------------------------------

COPY requirements.txt .
RUN pip install --no-cache-dir \
    torch==2.2.2+cu121 \
    torchvision==0.17.2+cu121 \
    --index-url https://download.pytorch.org/whl/cu121

RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------------------------------------------------------
# Copy Hi3DGen Python code
# -----------------------------------------------------------------------------

COPY hi3dgen/ ./hi3dgen/

# -----------------------------------------------------------------------------
# Model weights handling
# -----------------------------------------------------------------------------
# Models are NOT copied into the image (they're too large for GitHub).
# Instead, handler.py will download them from HuggingFace at container startup.
# This happens once per container, so subsequent requests are fast.
#
# If you want to bake models into the image (faster cold starts):
# 1. Download models locally using download_models.py
# 2. Uncomment the COPY commands below
# 3. Build locally: docker build -t yourname/hi3dgen-worker:tag .
# 4. Push to Docker Hub and update RunPod to use that image
#
# COPY hi3dgen/trellis-normal-v0-1/ /models/hi3dgen/trellis-normal-v0-1/
# COPY hi3dgen/yoso-normal-v1-8-1/ /models/hi3dgen/yoso-normal-v1-8-1/
# COPY hi3dgen/BiRefNet/ /models/hi3dgen/BiRefNet/

# -----------------------------------------------------------------------------
# Copy worker code
# -----------------------------------------------------------------------------

COPY handler.py .

# -----------------------------------------------------------------------------
# Hard sanity check (fails build if CUDA missing)
# -----------------------------------------------------------------------------

RUN python - <<'EOF'
import torch
assert torch.cuda.is_available(), "CUDA NOT AVAILABLE — BUILD INVALID"
print("CUDA OK:", torch.cuda.get_device_name(0))
EOF

# -----------------------------------------------------------------------------
# RunPod serverless entry
# -----------------------------------------------------------------------------

CMD ["python", "handler.py"]
