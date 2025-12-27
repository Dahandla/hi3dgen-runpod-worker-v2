FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Install system dependencies including build tools for CUDA extensions
RUN apt-get update && apt-get install -y \
    python3 python3-pip git \
    libgl1 libglib2.0-0 \
    build-essential \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch with CUDA 12.4 first
RUN pip3 install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124

# Install spconv and xformers (must be before other requirements)
RUN pip3 install spconv-cu120==2.3.6 || echo "Warning: spconv installation failed, may need manual build"
RUN pip3 install -U xformers --index-url https://download.pytorch.org/whl/cu124 || echo "Warning: xformers installation failed"

# Install other requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy custom extensions (must be after PyTorch is installed)
# Note: This is a standalone repo - all packages are included

# Custom rasterizer (CUDA extension)
COPY hy3dgen/texgen/custom_rasterizer /app/hy3dgen/texgen/custom_rasterizer
WORKDIR /app/hy3dgen/texgen/custom_rasterizer
RUN pip3 install --no-build-isolation -e . || echo "Warning: custom_rasterizer installation failed"

# Differentiable renderer (C++ extension)
WORKDIR /app
COPY hy3dgen/texgen/differentiable_renderer /app/hy3dgen/texgen/differentiable_renderer
WORKDIR /app/hy3dgen/texgen/differentiable_renderer
RUN pip3 install --no-build-isolation -e . || echo "Warning: differentiable_renderer installation failed"

# Copy application code
WORKDIR /app
COPY handler.py /app/
COPY pipeline /app/pipeline
COPY utils /app/utils
COPY models /models

# Copy hi3dgen and hy3dgen packages (needed for imports)
COPY hi3dgen /app/hi3dgen
COPY hy3dgen /app/hy3dgen

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:${PYTHONPATH}

# Note: RunPod serverless imports handler() function directly
# This CMD is a fallback for local testing
CMD ["python3", "-c", "from handler import handler; print('Handler ready')"]

