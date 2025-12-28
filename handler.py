import runpod
import trimesh
import tempfile
import base64
import os

def handler(event):
    # Create a simple cube
    mesh = trimesh.creation.box(extents=(1, 1, 1))

    # Write GLB to temp file
    with tempfile.NamedTemporaryFile(suffix=".glb", delete=False) as f:
        mesh.export(f.name)
        glb_path = f.name

    # Read & encode
    with open(glb_path, "rb") as f:
        glb_bytes = f.read()

    glb_b64 = base64.b64encode(glb_bytes).decode("utf-8")

    os.remove(glb_path)

    return {
        "status": "completed",
        "result": {
            "mesh_glb_base64": glb_b64,
            "mesh_name": "Hi3DGen_DummyCube"
        }
    }

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
