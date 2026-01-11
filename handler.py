<<<<<<< HEAD
"""
RunPod Serverless Handler - Minimal Dummy Worker
Creates a simple cube and returns it as base64-encoded GLB.
This is a minimal test to verify RunPod serverless lifecycle.
"""

import base64
import io
import trimesh
import runpod


def handler(event):
    """
    RunPod serverless handler entry point.
    
    Creates a simple cube mesh, exports to GLB, and returns base64-encoded.
    
    Args:
        event: RunPod event dict with 'input' key
        
    Returns:
        dict: Response with status, mesh_glb_base64, and debug info
    """
    try:
        # Create a simple cube mesh
        mesh = trimesh.creation.box(extents=(1.0, 1.0, 1.0))
        
        # Export to GLB in memory
        glb_bytes = trimesh.exchange.gltf.export_glb(mesh)
        
        # Encode to base64
        glb_b64 = base64.b64encode(glb_bytes).decode("utf-8")
        
        return {
            "status": "success",
            "mesh_glb_base64": glb_b64,
            "debug": {
                "vertices": len(mesh.vertices),
                "faces": len(mesh.faces),
                "glb_size_bytes": len(glb_bytes)
            }
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "status": "failed",
            "error": {
                "code": "HANDLER_ERROR",
                "message": str(e),
                "retryable": True
            }
        }

=======
import runpod
import trimesh
import tempfile
import base64
import os

def handler(event):
    # Create a simple cube
    mesh = trimesh.creation.box(extents=(1, 1, 1))

    # Export to temp GLB
    with tempfile.NamedTemporaryFile(suffix=".glb", delete=False) as f:
        mesh.export(f.name)
        glb_path = f.name

    # Encode GLB
    with open(glb_path, "rb") as f:
        glb_b64 = base64.b64encode(f.read()).decode("utf-8")

    os.remove(glb_path)

    return {
        "status": "completed",
        "result": {
            "mesh_glb_base64": glb_b64,
            "mesh_name": "Hi3DGen_DummyCube"
        }
    }
>>>>>>> 22b166206e16b761343add9d580dbfd18d339e66

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
