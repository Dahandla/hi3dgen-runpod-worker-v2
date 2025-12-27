# What is Zero123? (And Do You Need It?)

## What is Zero123?

**Zero123** is an AI model for **novel view synthesis** - it takes a single image of an object and generates what that object would look like from different camera angles.

### Key Features:
- **Input**: One image of an object
- **Output**: Multiple images showing the same object from different viewpoints (front, back, left, right, top, bottom, etc.)
- **Purpose**: Generate multiple views needed for 3D reconstruction

### Example:
```
Input:  [Photo of a chair from front]
           ↓
    Zero123 Model
           ↓
Output: [Front view] [Side view] [Back view] [Top view]
```

## Why Multiview is Needed

To create a 3D mesh, you typically need:
1. **Multiple views** of the object (from different angles)
2. **3D reconstruction** from those views
3. **Texture generation** for the mesh

The multiview stage generates those multiple camera angles.

---

## Do You Actually Need Zero123?

**Short answer: Probably NOT!** 

Looking at your codebase, you're using **Hunyuan3D**, which has its own multiview generation built-in.

### Your Current Setup

Your project uses:

1. **Hunyuan3D's Multiview Generation** (in `hy3dgen/texgen/utils/multiview_utils.py`)
   - `Multiview_Diffusion_Net` class
   - Part of the Hunyuan3D Paint pipeline
   - Already integrated in your codebase

2. **Hi3DGen/Hunyuan3D Shape Generation** (in `hy3dgen/shapegen/pipelines.py`)
   - `Hunyuan3DDiTPipeline` class
   - Can generate 3D meshes directly from images
   - May not require separate multiview generation

### When You Would Need Zero123

You'd only need Zero123 if:
- ❌ Hunyuan3D's multiview generation doesn't work well for your use case
- ❌ You want to use a different multiview model
- ❌ You're doing a custom pipeline that requires Zero123 specifically

**For most cases, you can skip Zero123 and use Hunyuan3D's built-in multiview generation.**

---

## How Your Pipeline Actually Works

Based on your codebase, here's what you're likely using:

### Option 1: Hunyuan3D Direct (Recommended)
```
Input Image
    ↓
Hunyuan3D Shape Pipeline → 3D Mesh (directly)
    ↓
Hunyuan3D Paint Pipeline → Textures
```

**No separate multiview step needed!** Hunyuan3D can generate meshes directly from a single image.

### Option 2: With Multiview (If Needed)
```
Input Image
    ↓
Hunyuan3D Multiview Diffusion → Multiple Views
    ↓
Hunyuan3D Shape Pipeline → 3D Mesh
    ↓
Hunyuan3D Paint Pipeline → Textures
```

Uses Hunyuan3D's own `Multiview_Diffusion_Net`, not Zero123.

---

## Implementation Recommendation

### For `pipeline/multiview.py`:

**Option A: Skip Multiview (Simplest)**
If Hunyuan3D can generate meshes directly from a single image:

```python
def generate_views(image_url, workdir):
    """
    For Hunyuan3D, we might not need separate multiview generation.
    Just return the input image - the mesh generation will handle it.
    """
    # Download input image
    response = requests.get(image_url)
    response.raise_for_status()
    
    img = Image.open(io.BytesIO(response.content))
    input_path = os.path.join(workdir, "input.jpg")
    img.save(input_path)
    
    return {
        "input_path": input_path,
        "views_dir": workdir,  # Same directory
        "num_views": 1,  # Just the input image
        "view_paths": [input_path]  # Single view
    }
```

**Option B: Use Hunyuan3D's Multiview (If Needed)**
If you need multiple views for better mesh quality:

```python
from hy3dgen.texgen.utils.multiview_utils import Multiview_Diffusion_Net
from hy3dgen.texgen.pipelines import Hunyuan3DTexGenConfig

def generate_views(image_url, workdir):
    """
    Use Hunyuan3D's built-in multiview generation.
    """
    # Download input image
    response = requests.get(image_url)
    response.raise_for_status()
    
    img = Image.open(io.BytesIO(response.content))
    input_path = os.path.join(workdir, "input.jpg")
    img.save(input_path)
    
    # Load Hunyuan3D multiview model
    config = Hunyuan3DTexGenConfig(
        light_remover_ckpt_path="/models/hunyuan3d-paint/hunyuan3d-delight-v2-0",
        multiview_ckpt_path="/models/hunyuan3d-paint/hunyuan3d-paint-v2-0-turbo",
        subfolder_name="hunyuan3d-paint-v2-0-turbo"
    )
    
    multiview_model = Multiview_Diffusion_Net(config)
    
    # Generate views (you'll need to set up camera angles)
    # This is more complex - see hy3dgen/texgen/pipelines.py for examples
    
    views_dir = os.path.join(workdir, "views")
    os.makedirs(views_dir, exist_ok=True)
    
    # TODO: Implement actual multiview generation using multiview_model
    # See hy3dgen/texgen/pipelines.py for how it's used
    
    return {
        "input_path": input_path,
        "views_dir": views_dir,
        "num_views": 4,
        "view_paths": [...]  # Generated view paths
    }
```

---

## Summary

| Model | Purpose | Do You Need It? |
|-------|---------|----------------|
| **Zero123** | Novel view synthesis (separate model) | ❌ **No** - You have Hunyuan3D's multiview |
| **Hunyuan3D Multiview** | Built-in multiview generation | ⚠️ **Maybe** - Only if you need multiple views |
| **Hunyuan3D Shape** | Direct mesh generation | ✅ **Yes** - This is your main model |
| **Hunyuan3D Paint** | Texture generation | ✅ **Yes** - For PBR textures |

---

## Recommendation for Your Implementation

1. **Start Simple**: Try generating meshes directly from a single image using Hunyuan3D Shape Pipeline
   - If quality is good → Skip multiview step entirely
   - If quality needs improvement → Add multiview generation

2. **Use Hunyuan3D's Multiview**: If you need multiview, use `Multiview_Diffusion_Net` from your codebase
   - It's already integrated
   - No need to download Zero123
   - Works with your existing models

3. **Skip Zero123**: Unless you have a specific reason, you don't need it

---

## Updated Model Directory Structure

You probably only need:

```
models/
├── hi3dgen/  # or hunyuan3d-dit (for mesh generation)
│   └── ... (Hunyuan3D shape model)
└── hunyuan3d-paint/  # (for texture generation)
    ├── hunyuan3d-delight-v2-0/
    └── hunyuan3d-paint-v2-0-turbo/
```

**No `zero123/` directory needed!**

---

## Next Steps

1. **Check your models**: Do you have Hunyuan3D models? (Hunyuan3D-2, Hunyuan3D-2mini, etc.)
2. **Test direct generation**: Try generating a mesh from a single image first
3. **Add multiview if needed**: Only if direct generation quality isn't good enough
4. **Use Hunyuan3D's multiview**: Not Zero123

---

## References

- **Zero123 Paper**: "Zero-1-to-3: Zero-shot One Image to 3D Object" (ICCV 2023)
- **Your Codebase**: `hy3dgen/texgen/utils/multiview_utils.py` - Hunyuan3D's multiview implementation
- **Your Codebase**: `hy3dgen/shapegen/pipelines.py` - Hunyuan3D's mesh generation

**Bottom line**: Zero123 is mentioned in the documentation as an option, but you're using Hunyuan3D which has its own (better integrated) multiview generation. You can safely ignore Zero123 for now! 🎯

