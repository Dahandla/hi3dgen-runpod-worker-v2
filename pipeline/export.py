"""
Output export and meta.json generation.

Creates the final output structure that Blender expects.
Contract-locked: must match exactly what the client validates.
"""

import json
import os
import shutil


def export_outputs(mesh, textures, workdir, job_id):
    """
    Export final outputs and create meta.json.
    
    Args:
        mesh: Mesh data dict with mesh_path
        textures: Texture dict with all texture paths
        workdir: Working directory
        job_id: Job identifier
        
    Returns:
        str: Path to meta.json
    """
    # Create output structure
    mesh_dir = os.path.join(workdir, "mesh")
    textures_dir = os.path.join(workdir, "textures")
    
    os.makedirs(mesh_dir, exist_ok=True)
    os.makedirs(textures_dir, exist_ok=True)
    
    # Copy mesh to final location
    if os.path.exists(mesh["mesh_path"]):
        final_mesh = os.path.join(mesh_dir, "hi3dgen_result.glb")
        shutil.copy2(mesh["mesh_path"], final_mesh)
    
    # Copy textures to final location
    for tex_type, tex_path in textures.items():
        if os.path.exists(tex_path):
            final_tex = os.path.join(textures_dir, f"{tex_type}.png")
            shutil.copy2(tex_path, final_tex)
    
    # Create meta.json (contract-locked format)
    meta = {
        "job_id": job_id,
        "status": "completed",
        "engine": "hi3dgen",
        "engine_version": "1.0",
        "outputs": {
            "mesh": "mesh/hi3dgen_result.glb",
            "textures": {
                "albedo": "textures/albedo.png",
                "normal": "textures/normal.png",
                "roughness": "textures/roughness.png",
                "metallic": "textures/metallic.png",
                "ao": "textures/ao.png"
            }
        }
    }
    
    meta_path = os.path.join(workdir, "meta.json")
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)
    
    return meta_path

