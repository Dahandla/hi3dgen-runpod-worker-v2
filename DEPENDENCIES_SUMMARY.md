# Dependencies Summary

This document summarizes the dependency setup for the Hi3DGen RunPod Worker.

## What Was Updated

### 1. Complete Requirements File (`requirements.txt`)

Updated from minimal to comprehensive, including:
- **Core PyTorch** (with CUDA 12.4 support)
- **ML/Deep Learning** libraries (transformers, diffusers, accelerate, etc.)
- **3D Processing** libraries (trimesh, pymeshlab, pygltflib, open3d, etc.)
- **Computer Vision** libraries (opencv, rembg, realesrgan, etc.)
- **Scientific Computing** (numpy, scipy, pandas, einops)
- **Cloud Storage** (boto3, requests)

**Excluded** (not needed on server):
- `bpy` (Blender Python API - client-side only)
- `gradio` (GUI framework)
- `fastapi/uvicorn` (RunPod handles HTTP)
- `PySide6` (GUI)
- `pythreejs` (browser visualization)

### 2. Special Dependencies

These must be installed separately due to CUDA version requirements:

- **spconv-cu120==2.3.6** - Sparse convolution (CUDA 12.0)
- **xformers** - Optimized attention operations

### 3. Dockerfile Updates

Updated to handle special dependencies:
- Install PyTorch first
- Install spconv and xformers before other requirements
- Graceful fallback if optional dependencies fail

### 4. Testing & Validation

Created comprehensive testing tools:
- **`test_dependencies.py`** - Validates all dependencies
- **`INSTALL.md`** - Complete installation guide
- **`setup_conda_env.sh`** - Automated setup script (Linux/Mac)
- **`setup_conda_env.bat`** - Automated setup script (Windows)

## Installation Order

1. **PyTorch** (with CUDA 12.4)
2. **spconv** (CUDA 12.0 build)
3. **xformers** (optimized attention)
4. **Other requirements** (from requirements.txt)

## Testing

Run the test script to verify everything:

```bash
python test_dependencies.py
```

This will:
- Test all imports
- Check CUDA availability
- Report missing dependencies
- Show versions of installed packages

## Key Dependencies by Category

### Required for Core Pipeline
- torch, torchvision, torchaudio
- transformers, diffusers, accelerate
- trimesh, pygltflib, pymeshlab
- numpy, scipy, einops
- PIL/Pillow, opencv-python

### Required for Texture Generation
- rembg, realesrgan, basicsr
- facexlib, gfpgan
- Custom rasterizer (compiled)

### Required for Mesh Processing
- trimesh, pymeshlab
- open3d, xatlas
- pygltflib

### Optional but Recommended
- spconv (for sparse convolutions)
- xformers (for optimized attention)
- cupy (for GPU computing)

### Cloud/Storage
- boto3 (S3-compatible storage)
- requests (HTTP client)

## Notes

- All version pins match the original project requirements
- CUDA 12.x is required for GPU acceleration
- Some dependencies may need compilation (custom rasterizer)
- Docker builds should handle most dependencies automatically

## Next Steps

1. Test the conda environment setup locally
2. Verify all dependencies install correctly
3. Test imports with `test_dependencies.py`
4. Build Docker image and verify it works
5. Deploy to RunPod

