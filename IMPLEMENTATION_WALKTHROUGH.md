# Implementation Walkthrough: From Placeholders to Production

This guide walks you through implementing the RunPod worker from its current placeholder state to a fully functional production system.

## Overview

Your RunPod worker currently has:
- ✅ Complete infrastructure (handler, utils, export)
- ✅ Pipeline structure (multiview → mesh → texture → export)
- ⚠️ Placeholder implementations in pipeline modules
- ⚠️ Empty models directory

**Goal**: Replace placeholders with actual model inference code.

---

## Step 1: Understand the Pipeline Flow

The pipeline runs in this order:

```
Input Image URL
    ↓
[multiview.py] → Generate multiple views (Zero123/Hi3DGen)
    ↓
[mesh.py] → Build 3D mesh from views
    ↓
[texture.py] → Bake PBR textures (albedo, normal, roughness, metallic, AO)
    ↓
[export.py] → Create meta.json and organize outputs
    ↓
[storage.py] → Upload to S3
    ↓
Return meta.json URL to Blender addon
```

Each module receives data from the previous stage and returns a dict for the next stage.

---

## Step 2: Implement Pipeline Modules

### 2.1 Multiview Generation (`pipeline/multiview.py`)

**Current State**: Downloads image, creates placeholder structure

**What to Implement**:
- Load Zero123 or Hi3DGen multiview model
- Generate multiple camera views from input image
- Save view images to `views_dir`
- Return view data with camera parameters

**Example Implementation Structure**:

```python
import os
import requests
import torch
from PIL import Image
import io
from hy3dgen.shapegen.pipelines import Hunyuan3DDiTPipeline  # or your model

# Global model instance (loaded once, reused)
_model = None

def _load_model():
    """Load model once, reuse for all requests."""
    global _model
    if _model is None:
        model_path = "/models/hi3dgen"  # or your model path
        _model = Hunyuan3DDiTPipeline.from_pretrained(model_path)
        _model = _model.to("cuda")
        _model.eval()
    return _model

def generate_views(image_url, workdir):
    """
    Generate multiview images from input image.
    
    Returns:
        dict: {
            "input_path": str,
            "views_dir": str,
            "num_views": int,
            "view_paths": [str, ...],  # List of view image paths
            "cameras": [...],  # Camera parameters if needed
        }
    """
    # Download input image
    response = requests.get(image_url)
    response.raise_for_status()
    
    img = Image.open(io.BytesIO(response.content))
    input_path = os.path.join(workdir, "input.jpg")
    img.save(input_path)
    
    # Load model
    model = _load_model()
    
    # Generate views
    views_dir = os.path.join(workdir, "views")
    os.makedirs(views_dir, exist_ok=True)
    
    # TODO: Replace with actual multiview generation
    # Example pseudocode:
    # views = model.generate_multiview(input_path, num_views=4)
    # for i, view in enumerate(views):
    #     view_path = os.path.join(views_dir, f"view_{i:03d}.jpg")
    #     view.save(view_path)
    
    # For now, return structure (replace with actual generation)
    view_paths = [
        os.path.join(views_dir, f"view_{i:03d}.jpg")
        for i in range(4)
    ]
    
    return {
        "input_path": input_path,
        "views_dir": views_dir,
        "num_views": 4,
        "view_paths": view_paths,
        "cameras": []  # Add camera parameters if needed
    }
```

**Key Points**:
- Load model once (use global variable or singleton)
- Generate multiple views (typically 4-6 views)
- Save views to `views_dir`
- Return dict with paths and metadata

---

### 2.2 Mesh Generation (`pipeline/mesh.py`)

**Current State**: Creates empty mesh directory

**What to Implement**:
- Load Hi3DGen mesh generation model
- Generate 3D mesh from multiview images
- Export mesh as GLB file
- Return mesh path

**Example Implementation Structure**:

```python
import os
import torch
import trimesh
from hy3dgen.shapegen.pipelines import Hunyuan3DDiTPipeline  # or your model

# Global model instance
_mesh_model = None

def _load_mesh_model():
    """Load mesh generation model."""
    global _mesh_model
    if _mesh_model is None:
        model_path = "/models/hi3dgen"
        _mesh_model = Hunyuan3DDiTPipeline.from_pretrained(model_path)
        _mesh_model = _mesh_model.to("cuda")
        _mesh_model.eval()
    return _mesh_model

def build_mesh(views, workdir):
    """
    Build 3D mesh from multiview images.
    
    Args:
        views: dict from generate_views() with view_paths, etc.
        workdir: Working directory
    
    Returns:
        dict: {
            "mesh_path": str,  # Path to GLB file
            "mesh_dir": str,
        }
    """
    mesh_dir = os.path.join(workdir, "mesh")
    os.makedirs(mesh_dir, exist_ok=True)
    
    # Load model
    model = _load_mesh_model()
    
    # Get view images
    view_paths = views.get("view_paths", [])
    input_path = views.get("input_path")
    
    # TODO: Replace with actual mesh generation
    # Example pseudocode:
    # mesh = model.generate_mesh(
    #     input_image=input_path,
    #     multiview_images=view_paths,
    #     resolution=256,  # or from config
    # )
    # 
    # # Export to GLB
    # mesh_path = os.path.join(mesh_dir, "hi3dgen_result.glb")
    # mesh.export(mesh_path)
    
    # For now, create placeholder (replace with actual generation)
    mesh_path = os.path.join(mesh_dir, "hi3dgen_result.glb")
    
    # Create a minimal placeholder mesh (remove this in production)
    # This is just to test the pipeline structure
    # mesh = trimesh.creation.box()
    # mesh.export(mesh_path)
    
    return {
        "mesh_path": mesh_path,
        "mesh_dir": mesh_dir
    }
```

**Key Points**:
- Use multiview images from previous stage
- Generate mesh using Hi3DGen model
- Export as GLB format (required by Blender addon)
- Save to `mesh_dir/hi3dgen_result.glb`

---

### 2.3 Texture Baking (`pipeline/texture.py`)

**Current State**: Creates empty texture directory structure

**What to Implement**:
- Load texture generation model (Hunyuan3D Paint)
- Generate PBR textures from mesh and views
- Save textures: albedo, normal, roughness, metallic, AO
- Return texture paths

**Example Implementation Structure**:

```python
import os
import torch
from hy3dgen.texgen.pipelines import Hunyuan3DPaintPipeline

# Global model instance
_texture_model = None

def _load_texture_model():
    """Load texture generation model."""
    global _texture_model
    if _texture_model is None:
        model_path = "/models/hunyuan3d-paint"  # or your model path
        _texture_model = Hunyuan3DPaintPipeline.from_pretrained(
            model_path,
            subfolder='hunyuan3d-paint-v2-0-turbo'
        )
    return _texture_model

def bake_textures(mesh, workdir):
    """
    Bake textures for the generated mesh.
    
    Args:
        mesh: dict from build_mesh() with mesh_path
        workdir: Working directory
    
    Returns:
        dict: {
            "albedo": str,  # Path to albedo.png
            "normal": str,  # Path to normal.png
            "roughness": str,  # Path to roughness.png
            "metallic": str,  # Path to metallic.png
            "ao": str,  # Path to ao.png
        }
    """
    textures_dir = os.path.join(workdir, "textures")
    os.makedirs(textures_dir, exist_ok=True)
    
    # Load model
    model = _load_texture_model()
    
    # Get mesh path
    mesh_path = mesh.get("mesh_path")
    
    # TODO: Replace with actual texture baking
    # Example pseudocode:
    # textures = model.bake_textures(
    #     mesh_path=mesh_path,
    #     texture_size=2048,  # or from config
    # )
    # 
    # # Save each texture
    # textures["albedo"].save(os.path.join(textures_dir, "albedo.png"))
    # textures["normal"].save(os.path.join(textures_dir, "normal.png"))
    # textures["roughness"].save(os.path.join(textures_dir, "roughness.png"))
    # textures["metallic"].save(os.path.join(textures_dir, "metallic.png"))
    # textures["ao"].save(os.path.join(textures_dir, "ao.png"))
    
    # For now, return structure (replace with actual generation)
    textures = {
        "albedo": os.path.join(textures_dir, "albedo.png"),
        "normal": os.path.join(textures_dir, "normal.png"),
        "roughness": os.path.join(textures_dir, "roughness.png"),
        "metallic": os.path.join(textures_dir, "metallic.png"),
        "ao": os.path.join(textures_dir, "ao.png")
    }
    
    return textures
```

**Key Points**:
- Use Hunyuan3D Paint pipeline for texture generation
- Generate all 5 PBR textures (albedo, normal, roughness, metallic, AO)
- Save as PNG files
- Return dict with all texture paths

---

## Step 3: Add Model Weights

### 3.1 Download Model Weights

You need to download the model weights and place them in the `models/` directory:

```bash
# From project root
cd hi3dgen-runpod-worker/models

# Create directories
mkdir -p hi3dgen
mkdir -p zero123  # if needed
mkdir -p hunyuan3d-paint  # for texture generation
```

### 3.2 Model Locations

**Hi3DGen Model** (for mesh generation):
- Download from: [Your model source]
- Place in: `models/hi3dgen/`
- Should contain: model weights, config files

**Hunyuan3D Paint Model** (for texture generation):
- Download from: HuggingFace or your source
- Place in: `models/hunyuan3d-paint/`
- Should contain:
  - `hunyuan3d-delight-v2-0/` (light removal)
  - `hunyuan3d-paint-v2-0-turbo/` (texture generation)

**Zero123 Model** (for multiview, if not using Hi3DGen):
- Download from: [Your model source]
- Place in: `models/zero123/`

### 3.3 Update Model Paths in Code

Update the model paths in your pipeline modules:

```python
# In multiview.py, mesh.py, texture.py
MODEL_BASE_PATH = "/models"  # In Docker, models are at /models

# For Hi3DGen
HI3DGEN_MODEL_PATH = os.path.join(MODEL_BASE_PATH, "hi3dgen")

# For Hunyuan3D Paint
HUNYUAN3D_PAINT_PATH = os.path.join(MODEL_BASE_PATH, "hunyuan3d-paint")
```

### 3.4 Verify Model Structure

Your `models/` directory should look like:

```
models/
├── hi3dgen/
│   ├── config.yaml
│   ├── model.safetensors
│   └── ... (other model files)
├── hunyuan3d-paint/
│   ├── hunyuan3d-delight-v2-0/
│   │   └── ... (delight model files)
│   └── hunyuan3d-paint-v2-0-turbo/
│       └── ... (paint model files)
└── zero123/  # if needed
    └── ... (zero123 model files)
```

---

## Step 4: Test Docker Build Locally

### 4.1 Build the Docker Image

```bash
# From project root directory
docker build -f hi3dgen-runpod-worker/Dockerfile -t hi3dgen-runpod-worker:latest .
```

**What to Watch For**:
- ✅ PyTorch installs successfully
- ✅ spconv and xformers install
- ✅ Custom rasterizer compiles (may take 5-10 minutes)
- ✅ Differentiable renderer compiles (may take 2-5 minutes)
- ✅ All requirements install
- ✅ Models are copied into image

**Common Issues**:
- **CUDA compilation errors**: Check CUDA version matches base image
- **spconv fails**: May need to build from source
- **Out of memory**: Increase Docker memory limit
- **Model files missing**: Check COPY commands in Dockerfile

### 4.2 Test Handler Import

```bash
docker run --rm hi3dgen-runpod-worker:latest \
  python3 -c "from handler import handler; print('Handler ready')"
```

Should output: `Handler ready`

### 4.3 Test Model Loading (Optional)

Create a test script to verify models load:

```python
# test_models.py
import torch
from hy3dgen.shapegen.pipelines import Hunyuan3DDiTPipeline

print("Testing model loading...")
model = Hunyuan3DDiTPipeline.from_pretrained("/models/hi3dgen")
print("✓ Model loaded successfully")
```

Run in Docker:
```bash
docker run --rm hi3dgen-runpod-worker:latest python3 test_models.py
```

---

## Step 5: Follow Deployment Checklist

### 5.1 Pre-Deployment

Follow `DEPLOYMENT_CHECKLIST.md` section by section:

1. **Code Structure** ✅ (already done)
2. **Model Weights** ⚠️ (add your models)
3. **Pipeline Implementation** ⚠️ (implement placeholders)
4. **Environment Variables** (prepare S3 credentials)
5. **S3 Storage Setup** (create bucket, test access)

### 5.2 Docker Build

1. Build image locally
2. Test handler import
3. Check image size (should be reasonable)
4. Tag and push to registry

### 5.3 RunPod Deployment

1. Create serverless endpoint in RunPod console
2. Set environment variables (S3 credentials)
3. Configure GPU type (A10 recommended)
4. Set timeout (300 seconds)
5. Deploy image

### 5.4 Testing

1. Get endpoint URL from RunPod
2. Test with simple request (use curl or Postman)
3. Verify response format
4. Check RunPod logs for errors

### 5.5 Blender Addon Integration

1. Open Blender addon preferences
2. Set backend to "REMOTE"
3. Paste RunPod endpoint URL
4. Submit test job
5. Verify mesh and textures download

---

## Step 6: Implementation Tips

### 6.1 Model Loading Strategy

**Option 1: Load on First Request** (Recommended for serverless)
```python
_model = None

def get_model():
    global _model
    if _model is None:
        _model = load_model()
    return _model
```

**Option 2: Pre-load in Handler** (If cold starts are acceptable)
```python
# In handler.py
_model = load_model()  # Load once when handler module imports

def handler(event):
    # Use _model directly
```

### 6.2 Error Handling

Always wrap model inference in try/except:

```python
try:
    result = model.generate(...)
except Exception as e:
    raise RuntimeError(f"Model inference failed: {e}")
```

### 6.3 Memory Management

Clear GPU cache between stages:

```python
import torch

# After each stage
torch.cuda.empty_cache()
```

### 6.4 Progress Logging

Use the progress utility:

```python
from utils.progress import log_progress

log_progress("multiview", 25, "Generating views...")
log_progress("mesh", 50, "Building mesh...")
log_progress("texture", 75, "Baking textures...")
```

### 6.5 Time Limits

The pipeline has a 180-second hard cap. Adjust if needed:

```python
# In pipeline/run.py
MAX_SECONDS = 300  # 5 minutes
```

---

## Step 7: Testing Strategy

### 7.1 Unit Tests (Local)

Test each pipeline module individually:

```python
# test_multiview.py
from pipeline.multiview import generate_views

views = generate_views("https://example.com/image.jpg", "/tmp/test")
assert "view_paths" in views
assert len(views["view_paths"]) > 0
```

### 7.2 Integration Test (Local Docker)

Test full pipeline in Docker:

```python
# test_pipeline.py
from pipeline.run import run_pipeline

payload = {
    "api_version": "1.0",
    "input": {
        "image_url": "https://example.com/test.jpg"
    }
}

result = run_pipeline(payload)
assert "job_id" in result
assert "meta_url" in result
```

### 7.3 End-to-End Test (RunPod)

Test with actual RunPod endpoint:

```bash
curl -X POST https://your-endpoint.runpod.ai \
  -H "Content-Type: application/json" \
  -d '{
    "api_version": "1.0",
    "input": {
      "image_url": "https://example.com/test.jpg"
    }
  }'
```

---

## Step 8: Common Issues & Solutions

### Issue: Models Not Found

**Solution**: 
- Check model paths in code match Docker COPY paths
- Verify models are in `models/` directory before build
- Check file permissions

### Issue: CUDA Out of Memory

**Solution**:
- Reduce batch size
- Use smaller resolution
- Clear cache between stages: `torch.cuda.empty_cache()`

### Issue: Timeout Errors

**Solution**:
- Increase `MAX_SECONDS` in `pipeline/run.py`
- Increase RunPod endpoint timeout
- Optimize model inference (use smaller models, fewer steps)

### Issue: Custom Rasterizer Fails

**Solution**:
- Check CUDA toolkit version matches base image
- Verify nvcc is available in Docker build
- Check compilation logs for specific errors

### Issue: S3 Upload Fails

**Solution**:
- Verify environment variables are set in RunPod
- Test S3 credentials locally
- Check bucket permissions

---

## Next Steps

1. **Start with Multiview**: Implement `multiview.py` first (simplest)
2. **Then Mesh**: Implement `mesh.py` (core functionality)
3. **Finally Texture**: Implement `texture.py` (most complex)
4. **Test Each Stage**: Test each module before moving to next
5. **Add Models**: Download and add model weights
6. **Build Docker**: Test Docker build locally
7. **Deploy**: Follow deployment checklist
8. **Monitor**: Watch RunPod logs and optimize

---

## Resources

- **Pipeline Code**: `hy3dgen/shapegen/pipelines.py` and `hy3dgen/texgen/pipelines.py`
- **Model Loading**: Check existing code in `__init__.py` for examples
- **Deployment Checklist**: `DEPLOYMENT_CHECKLIST.md`
- **Docker Build**: See `Dockerfile` and `README.md`

---

## Questions?

If you get stuck:
1. Check RunPod worker logs
2. Test components individually
3. Review error messages carefully
4. Check model paths and file permissions
5. Verify all dependencies are installed

Good luck! 🚀

