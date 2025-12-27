# Installation Guide for Hi3DGen RunPod Worker

This guide covers setting up the development environment and testing dependencies before deployment.

## Prerequisites

- **Python 3.10** (required)
- **CUDA 12.x** (for GPU acceleration)
- **Miniconda** (recommended for environment management)
- **NVIDIA GPU** with CUDA support

## Step 1: Create Conda Environment

```bash
# Create conda environment
conda create -n hi3dgen-runpod python=3.10
conda activate hi3dgen-runpod
```

## Step 2: Install PyTorch with CUDA 12.4

```bash
# Install PyTorch with CUDA 12.4 support
pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124
```

## Step 3: Install Sparse Convolution (spconv)

```bash
# Install spconv for CUDA 12.0
pip install spconv-cu120==2.3.6
```

**Note**: If you have a different CUDA version, adjust accordingly:
- CUDA 11.8: `pip install spconv-cu118==2.3.6`
- CUDA 12.1: `pip install spconv-cu121==2.3.6`

## Step 4: Install XFormers (Optimized Attention)

```bash
# Install xformers for optimized attention operations
pip install -U xformers --index-url https://download.pytorch.org/whl/cu124
```

## Step 5: Install Core Requirements

```bash
# Install all other dependencies
pip install -r requirements.txt
```

## Step 6: Install Custom Rasterizer (REQUIRED for texture generation)

**IMPORTANT**: The custom rasterizer is required for the texture pipeline to work. Without it, you'll get the error: `module 'custom_rasterizer' has no attribute 'rasterize'`

### Option 1: Use the installation script (Recommended)

Run the provided script from the project root:

```bash
install_custom_rasterizer.bat
```

This script will:
- Find the custom_rasterizer directory automatically
- Install it in your conda environment
- Verify the installation

### Option 2: Manual installation

```bash
# Activate your conda environment
conda activate hi3dgen-runpod

# Navigate to the custom_rasterizer directory
# Path depends on where your addon is installed:
# For Blender addon: C:\Users\<user>\AppData\Roaming\Blender Foundation\Blender\4.5\scripts\addons\hi3dgenRemote_Backend\hy3dgen\texgen\custom_rasterizer
# For development: R:\AddOnPublish\Hi3DGen_PBR_AddOn_V2\hy3dpaint\custom_rasterizer

cd "path\to\hy3dgen\texgen\custom_rasterizer"
pip install -e .
```

**Requirements**:
- `nvcc` (NVIDIA CUDA Compiler) must be in your PATH
- CUDA toolkit installed
- Visual Studio Build Tools (Windows) or GCC (Linux) with C++ support
- PyTorch CUDA version must match your CUDA toolkit version

### Verification

After installation, verify it works:

```python
import custom_rasterizer
print(dir(custom_rasterizer))  # Should show 'rasterize' in the list
```

## Step 7: Install Differentiable Renderer (REQUIRED for texture generation)

**IMPORTANT**: The differentiable_renderer is also required for the texture pipeline. It provides mesh processing capabilities.

### Option 1: Use the installation script (Recommended)

Run the provided script from the project root:

```bash
install_differentiable_renderer.bat
```

This script will:
- Find the differentiable_renderer directory automatically
- Install it in your conda environment
- Verify the installation

### Option 2: Manual installation

```bash
# Activate your conda environment
conda activate hi3dgen-runpod

# Navigate to the differentiable_renderer directory
# Path depends on where your addon is installed:
# For Blender addon: C:\Users\<user>\AppData\Roaming\Blender Foundation\Blender\4.5\scripts\addons\hi3dgenRemote_Backend\hy3dgen\texgen\differentiable_renderer

cd "path\to\hy3dgen\texgen\differentiable_renderer"
pip install --no-build-isolation -e .
```

**Requirements**:
- C++ compiler (Visual Studio Build Tools on Windows, GCC on Linux)
- `pybind11` (should be in requirements.txt)
- Build tools in PATH

### Verification

After installation, verify it works:

```python
import mesh_processor
print("SUCCESS: mesh_processor imported")
```

## Step 8: Verify Installation

Run the test script to verify all dependencies:

```bash
python test_dependencies.py
```

## Docker Build Notes

When building the Docker image, the Dockerfile will:

1. Install system dependencies
2. Install Python requirements from `requirements.txt`
3. Copy your code and models

**Important**: For Docker builds, you may need to:

1. Pre-install spconv and xformers in a base image, OR
2. Use a multi-stage build, OR
3. Install them separately in the Dockerfile before the main requirements

Example Dockerfile addition:

```dockerfile
# Install PyTorch first
RUN pip3 install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124

# Install spconv and xformers
RUN pip3 install spconv-cu120==2.3.6
RUN pip3 install -U xformers --index-url https://download.pytorch.org/whl/cu124

# Then install other requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
```

## Troubleshooting

### CUDA Version Mismatch

If you get CUDA version errors:
- Verify your CUDA version: `nvcc --version`
- Install matching spconv version: `spconv-cu{version}`

### XFormers Installation Fails

If xformers fails to install:
- Try without version pin: `pip install xformers`
- Or build from source if needed

### spconv Import Errors

If spconv doesn't import:
- Verify CUDA toolkit is installed
- Check that spconv version matches CUDA version
- Try: `python -c "import spconv; print(spconv.__version__)"`

### Out of Memory During Build

If Docker build runs out of memory:
- Increase Docker memory limit
- Use `--no-cache` flag: `docker build --no-cache ...`

## Testing the Environment

After installation, test imports:

```python
# Test core imports
import torch
import torchvision
import numpy as np
from PIL import Image

# Test ML libraries
import transformers
import diffusers
from diffusers import AutoPipelineForText2Image

# Test 3D processing
import trimesh
import pygltflib
import pymeshlab

# Test sparse convolution (if installed)
try:
    import spconv
    print(f"spconv version: {spconv.__version__}")
except ImportError:
    print("Warning: spconv not installed")

# Test xformers (if installed)
try:
    import xformers
    print(f"xformers available")
except ImportError:
    print("Warning: xformers not installed")

print("All core dependencies imported successfully!")
```

## Next Steps

1. Add your model weights to `models/` directory
2. Implement pipeline modules (`multiview.py`, `mesh.py`, `texture.py`)
3. Test locally before building Docker image
4. Build and deploy to RunPod

