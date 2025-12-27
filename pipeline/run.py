"""
Pipeline orchestrator with safety caps.

Coordinates the full pipeline: multiview → mesh → textures → export.
Enforces runtime limits to prevent runaway costs.
"""

import os
import uuid
import time
from pipeline.multiview import generate_views
from pipeline.mesh import build_mesh
from pipeline.texture import bake_textures
from pipeline.export import export_outputs
from utils.storage import upload_job

MAX_SECONDS = 180  # hard cap (Step 6 safety)


def run_pipeline(payload):
    """
    Run the complete Hi3DGen pipeline.
    
    Args:
        payload: Validated request payload with input.image_url
        
    Returns:
        dict: job_id and meta_url
    """
    job_id = f"job_{uuid.uuid4().hex[:16]}"
    start = time.time()

    workdir = f"/tmp/{job_id}"
    os.makedirs(workdir, exist_ok=True)

    image_url = payload["input"]["image_url"]

    # Pipeline stages with time checks
    views = generate_views(image_url, workdir)
    _check_time(start)

    mesh = build_mesh(views, workdir)
    _check_time(start)

    textures = bake_textures(mesh, workdir)
    _check_time(start)

    export_outputs(mesh, textures, workdir, job_id)

    meta_url = upload_job(job_id, workdir)

    return {
        "job_id": job_id,
        "meta_url": meta_url
    }


def _check_time(start):
    """Raise if runtime exceeds MAX_SECONDS."""
    if time.time() - start > MAX_SECONDS:
        raise RuntimeError("Job exceeded time limit")

