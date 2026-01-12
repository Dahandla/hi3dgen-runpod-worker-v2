"""
RunPod Serverless Handler - Phase 1: Hi3DGen Mesh Generation
Generates 3D mesh from input image using Hi3DGen pipeline.
Returns mesh as base64-encoded GLB (no textures, no UVs).
"""

import os
import base64
import io
import runpod
import trimesh
import torch
from PIL import Image

# -----------------------------------------------------------------------------
# Environment & cache locations (important for RunPod)
# -----------------------------------------------------------------------------

os.environ.setdefault("HF_HOME", "/models/hf")
os.environ.setdefault("TORCH_HOME", "/models/torch")
os.environ.setdefault("TRANSFORMERS_CACHE", "/models/hf")

# -----------------------------------------------------------------------------
# Load Hi3DGen ONCE (container startup)
# -----------------------------------------------------------------------------

print("[Worker] Initializing Hi3DGen pipeline (geometry only)...")

from hi3dgen.pipelines.hi3dgen import Hi3DGenPipeline

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

try:
    # Load Hi3DGen pipeline from local path (baked into Docker image)
    # Models should be at /models/hi3dgen with subdirectories:
    # - trellis-normal-v0-1/
    # - yoso-normal-v1-8-1/
    # - BiRefNet/
    model_path = "/models/hi3dgen"
    
    print(f"[Worker] Loading Hi3DGen from {model_path} on {DEVICE}...")
    
    # Check if local models exist
    import os
    trellis_path = f"{model_path}/trellis-normal-v0-1"
    yoso_path = f"{model_path}/yoso-normal-v1-8-1"
    
    # Try yoso first (newer), then trellis as fallback
    if os.path.exists(f"{yoso_path}/pipeline.json"):
        print(f"[Worker] Found yoso model at {yoso_path}")
        hi3dgen_pipe = Hi3DGenPipeline.from_pretrained(
            yoso_path,
            local_files_only=True
        )
    elif os.path.exists(f"{trellis_path}/pipeline.json"):
        print(f"[Worker] Found trellis model at {trellis_path}")
        hi3dgen_pipe = Hi3DGenPipeline.from_pretrained(
            trellis_path,
            local_files_only=True
        )
    elif os.path.exists(f"{model_path}/pipeline.json"):
        # Fallback: models at root level
        print(f"[Worker] Found model at {model_path}")
        hi3dgen_pipe = Hi3DGenPipeline.from_pretrained(
            model_path,
            local_files_only=True
        )
    else:
        print(f"[Worker] Local models not found, attempting HuggingFace...")
        # Try Stable-X repos (may require auth)
        try:
            hi3dgen_pipe = Hi3DGenPipeline.from_pretrained(
                "Stable-X/yoso-normal-v1-8-1"
            )
        except:
            hi3dgen_pipe = Hi3DGenPipeline.from_pretrained(
                "Stable-X/trellis-normal-v0-1"
            )
    
    # Move to device (pipeline handles eval mode internally)
    hi3dgen_pipe.to(DEVICE)
    
    print(f"[Worker] Hi3DGen loaded successfully on {DEVICE}")
except Exception as e:
    print(f"[Worker][ERROR] Failed to load Hi3DGen: {e}")
    import traceback
    traceback.print_exc()
    hi3dgen_pipe = None

# -----------------------------------------------------------------------------
# Job handler
# -----------------------------------------------------------------------------

def handler(event):
    """
    Phase 1:
    - Input: image_base64 (required), seed (optional), resolution (optional)
    - Output: GLB (mesh only, no textures)
    """
    
    if hi3dgen_pipe is None:
        return {
            "status": "failed",
            "error": {
                "code": "MODEL_NOT_LOADED",
                "message": "Hi3DGen pipeline failed to load at startup",
                "retryable": False
            }
        }
    
    try:
        # -------------------------------------------------------------
        # Parse input
        # -------------------------------------------------------------
        input_data = event.get("input", {})
        
        image_b64 = input_data.get("image_base64", None)
        seed = input_data.get("seed", -1)
        resolution = int(input_data.get("resolution", 512))
        
        if image_b64 is None:
            raise ValueError("Missing image_base64 in input")
        
        # Decode image
        image_bytes = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        print(f"[Worker] Processing image: {image.size}, seed={seed}, resolution={resolution}")
        
        # -------------------------------------------------------------
        # Run Hi3DGen (geometry only)
        # -------------------------------------------------------------
        print("[Worker] Running Hi3DGen inference...")
        
        with torch.no_grad():
            # For Phase 1, skip image preprocessing (BiRefNet) to avoid dependency issues
            # Preprocessing can be enabled later when BiRefNet model is available
            result = hi3dgen_pipe.run(
                image=image,
                num_samples=1,
                seed=seed if seed >= 0 else None,
                formats=['mesh'],
                preprocess_image=False  # Skip BiRefNet preprocessing for Phase 1
            )
        
        # Extract mesh from result
        if 'mesh' not in result or result['mesh'] is None:
            raise RuntimeError("Hi3DGen returned empty mesh")
        
        mesh_result = result['mesh']
        
        # Convert to trimesh if needed
        if hasattr(mesh_result, 'to_trimesh'):
            # MeshExtractResult object - convert to trimesh
            mesh = mesh_result.to_trimesh(transform_pose=False)
        elif isinstance(mesh_result, trimesh.Trimesh):
            # Already a trimesh object
            mesh = mesh_result
        else:
            # Try to extract vertices and faces
            if hasattr(mesh_result, 'vertices') and hasattr(mesh_result, 'faces'):
                vertices = mesh_result.vertices
                faces = mesh_result.faces
                if hasattr(vertices, 'detach'):
                    vertices = vertices.detach().cpu().numpy()
                if hasattr(faces, 'detach'):
                    faces = faces.detach().cpu().numpy()
                mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
            else:
                raise RuntimeError(f"Unknown mesh format: {type(mesh_result)}")
        
        # -------------------------------------------------------------
        # Clean and prepare mesh
        # -------------------------------------------------------------
        mesh.remove_duplicate_faces()
        mesh.remove_degenerate_faces()
        mesh.remove_unreferenced_vertices()
        mesh.rezero()
        
        # Compute normals for Blender sanity
        _ = mesh.vertex_normals
        
        # -------------------------------------------------------------
        # Export GLB (mesh only)
        # -------------------------------------------------------------
        glb_bytes = trimesh.exchange.gltf.export_glb(mesh)
        glb_b64 = base64.b64encode(glb_bytes).decode("utf-8")
        
        print(f"[Worker] Generated mesh: {len(mesh.vertices)} vertices, {len(mesh.faces)} faces")
        
        return {
            "status": "success",
            "mesh_glb_base64": glb_b64,
            "debug": {
                "vertices": int(len(mesh.vertices)),
                "faces": int(len(mesh.faces)),
                "device": DEVICE,
                "glb_size_bytes": len(glb_bytes)
            }
        }
        
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print(f"[Worker][ERROR] {tb}")
        
        return {
            "status": "failed",
            "error": {
                "code": "HANDLER_ERROR",
                "message": str(e),
                "retryable": True
            }
        }


# -----------------------------------------------------------------------------
# RunPod entry
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
