# Quick Start: Getting Your RunPod Worker Production-Ready

## Current Status ✅

Your worker has:
- ✅ Complete infrastructure (handler, utils, storage, validation)
- ✅ Pipeline structure (multiview → mesh → texture → export)
- ✅ Dockerfile with custom extensions
- ✅ Deployment checklist
- ⚠️ **Placeholder code** in 3 pipeline modules
- ⚠️ **Empty models directory**

## What You Need to Do (4 Steps)

### 1️⃣ Implement Pipeline Modules (2-4 hours)

Replace placeholders in these files:

**`pipeline/multiview.py`**
- Load Zero123/Hi3DGen model
- Generate 4-6 multiview images from input
- Return view paths and camera data

**`pipeline/mesh.py`**
- Load Hi3DGen mesh model
- Generate 3D mesh from multiview images
- Export as GLB file

**`pipeline/texture.py`**
- Load Hunyuan3D Paint model
- Generate PBR textures (albedo, normal, roughness, metallic, AO)
- Save as PNG files

**See**: `IMPLEMENTATION_WALKTHROUGH.md` for detailed code examples

---

### 2️⃣ Add Model Weights (30 minutes)

Download and place models in `models/` directory:

```bash
hi3dgen-runpod-worker/models/
├── hi3dgen/          # Mesh generation model
├── hunyuan3d-paint/ # Texture generation model
└── zero123/          # Multiview model (if needed)
```

**Model Sources**:
- Hi3DGen: [Your model source]
- Hunyuan3D Paint: HuggingFace `tencent/Hunyuan3D-2.1` or your source
- Zero123: [Your model source]

---

### 3️⃣ Test Docker Build (30 minutes)

```bash
# From project root
docker build -f hi3dgen-runpod-worker/Dockerfile -t hi3dgen-runpod-worker:latest .

# Test handler
docker run --rm hi3dgen-runpod-worker:latest \
  python3 -c "from handler import handler; print('OK')"
```

**Watch for**:
- ✅ Custom rasterizer compiles (5-10 min)
- ✅ Differentiable renderer compiles (2-5 min)
- ✅ All dependencies install
- ✅ Models copied successfully

---

### 4️⃣ Deploy to RunPod (30 minutes)

1. **Push to Registry**:
   ```bash
   docker tag hi3dgen-runpod-worker:latest your-registry/hi3dgen-runpod-worker:latest
   docker push your-registry/hi3dgen-runpod-worker:latest
   ```

2. **Create RunPod Endpoint**:
   - GPU: A10
   - Timeout: 300s
   - Image: `your-registry/hi3dgen-runpod-worker:latest`
   - Env vars: `S3_ENDPOINT`, `S3_KEY`, `S3_SECRET`, `S3_BUCKET`

3. **Test**:
   - Get endpoint URL
   - Submit test job from Blender addon
   - Verify results

**See**: `DEPLOYMENT_CHECKLIST.md` for complete steps

---

## Implementation Priority

### Phase 1: Basic Functionality (Start Here)
1. ✅ Implement `multiview.py` (simplest)
2. ✅ Implement `mesh.py` (core feature)
3. ✅ Test with mesh-only (skip textures)
4. ✅ Deploy and test

### Phase 2: Full Pipeline
5. ✅ Implement `texture.py`
6. ✅ Test full pipeline
7. ✅ Deploy and verify

---

## Quick Reference

### File Locations
- **Pipeline modules**: `hi3dgen-runpod-worker/pipeline/`
- **Models**: `hi3dgen-runpod-worker/models/`
- **Handler**: `hi3dgen-runpod-worker/handler.py`
- **Dockerfile**: `hi3dgen-runpod-worker/Dockerfile`

### Key Imports You'll Need
```python
# For mesh generation
from hy3dgen.shapegen.pipelines import Hunyuan3DDiTPipeline

# For texture generation
from hy3dgen.texgen.pipelines import Hunyuan3DPaintPipeline

# For mesh export
import trimesh
```

### Model Loading Pattern
```python
_model = None

def get_model():
    global _model
    if _model is None:
        _model = YourPipeline.from_pretrained("/models/your-model")
        _model = _model.to("cuda")
        _model.eval()
    return _model
```

### Expected Output Structure
```
/tmp/job_xxxxx/
├── input.jpg
├── views/
│   ├── view_000.jpg
│   ├── view_001.jpg
│   └── ...
├── mesh/
│   └── hi3dgen_result.glb
├── textures/
│   ├── albedo.png
│   ├── normal.png
│   ├── roughness.png
│   ├── metallic.png
│   └── ao.png
└── meta.json
```

---

## Time Estimate

- **Implementation**: 2-4 hours (depending on model complexity)
- **Model setup**: 30 minutes
- **Docker build/test**: 30 minutes
- **Deployment**: 30 minutes
- **Testing**: 1-2 hours

**Total**: ~5-8 hours to production-ready

---

## Need Help?

1. **Detailed walkthrough**: See `IMPLEMENTATION_WALKTHROUGH.md`
2. **Deployment steps**: See `DEPLOYMENT_CHECKLIST.md`
3. **Code examples**: Check `hy3dgen/shapegen/pipelines.py` and `hy3dgen/texgen/pipelines.py`
4. **Existing code**: Look at `__init__.py` for model loading examples

---

## Common First Steps

1. **Start with one module**: Implement `multiview.py` first
2. **Test locally**: Run each module function manually
3. **Add models**: Download one model, test loading
4. **Build Docker**: Test Docker build with one model
5. **Iterate**: Add next module, test, repeat

---

## Success Criteria

You're ready when:
- ✅ All 3 pipeline modules have real implementations
- ✅ Models are in `models/` directory
- ✅ Docker build completes successfully
- ✅ Handler imports without errors
- ✅ Test job completes and returns meta.json URL
- ✅ Blender addon can download and import results

---

**Ready to start?** Open `IMPLEMENTATION_WALKTHROUGH.md` for step-by-step code examples! 🚀

