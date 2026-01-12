# Hi3DGen RunPod Worker v2
Hi3DGen RunPod Serverless Endpoint (CUDA-Enabled)

**⚠️ CRITICAL: This worker REQUIRES GPU/CUDA. CPU instances will fail.**

## Requirements
- **GPU Required**: NVIDIA L4 / A10 / A100 / RTX class
- **CUDA 12.1+**: Base image includes CUDA runtime
- **PyTorch with CUDA**: torch==2.2.2+cu121
- **spconv-cu121**: Sparse convolution (CUDA-only, no CPU fallback)

## Files
- `handler.py` – RunPod serverless handler (update with actual Hi3DGen implementation)
- `Dockerfile` – CUDA-enabled image (nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04)
- `requirements.txt` – Core dependencies including spconv-cu121

## Dockerfile Features
- ✅ CUDA 12.1.1 base image
- ✅ CUDA-enabled PyTorch installation
- ✅ spconv-cu121 (sparse convolution for Hi3DGen)
- ✅ Build-time CUDA availability check (fails if CUDA missing)

## Deploy on RunPod

### 1. Build Requirements
- Ensure `hi3dgen` code is available (copy into worker directory or adjust Dockerfile COPY path)
- Update `handler.py` with actual Hi3DGen pipeline implementation

### 2. Create RunPod Endpoint
- **Endpoint Type**: Serverless
- **GPU Type**: NVIDIA L4 / A10 / A100 (NOT CPU)
- **Container Image**: Build from this Dockerfile
- **Environment**: No special env vars needed (CUDA detected automatically)

### 3. Verify Deployment
After deployment, check logs for:
```
CUDA OK: [GPU Name]
[Worker] Hi3DGen loaded successfully on cuda
```

If you see CPU-related errors or "not implemented for CPU ONLY build", the endpoint is using CPU workers - recreate with GPU.

## Troubleshooting

**Error: "not implemented for CPU ONLY build"**
- ❌ Endpoint is using CPU workers
- ✅ Recreate endpoint with GPU (L4/A10/A100)

**Error: "CUDA NOT AVAILABLE — BUILD INVALID"**
- ❌ Docker build failed CUDA check
- ✅ Verify base image: `nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04`

**Error: "spconv installation failed"**
- Check CUDA version compatibility
- Ensure `spconv-cu121` matches your CUDA version
