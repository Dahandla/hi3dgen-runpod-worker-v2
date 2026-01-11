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


if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
