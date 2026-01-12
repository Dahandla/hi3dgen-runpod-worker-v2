"""
Download Hi3DGen models for RunPod worker.
This script downloads all required model files and organizes them for Docker build.
"""

import os
import json
from pathlib import Path
from huggingface_hub import snapshot_download, hf_hub_download, login
from huggingface_hub.utils import HfHubHTTPError

# Configuration
OUTPUT_DIR = Path("Hi3DGen")
# Hi3DGen uses these model repositories
MODEL_REPOS = [
    "Stable-X/trellis-normal-v0-1",
    "Stable-X/yoso-normal-v1-8-1",
    "ZhengPeng7/BiRefNet",  # Background removal model
]
USE_TOKEN = True  # Set to True if you have HF token

def download_models():
    """Download Hi3DGen models from HuggingFace."""
    
    print(f"[Download] Starting Hi3DGen model download...")
    print(f"[Download] Output directory: {OUTPUT_DIR.absolute()}")
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    models_dir = OUTPUT_DIR / "models"
    models_dir.mkdir(exist_ok=True)
    
    # Check for HF token
    hf_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
    if USE_TOKEN and hf_token:
        print(f"[Download] Using HuggingFace token for authentication...")
        login(token=hf_token)
    elif USE_TOKEN:
        print(f"[Download] WARNING: No HF_TOKEN found. Trying without authentication...")
        print(f"[Download] If download fails, set HF_TOKEN environment variable")
    
    try:
        # Download each model repository
        print(f"[Download] Downloading {len(MODEL_REPOS)} model repositories...")
        
        for repo_id in MODEL_REPOS:
            print(f"\n[Download] Downloading {repo_id}...")
            try:
                # Download to subdirectory
                repo_name = repo_id.split("/")[-1]
                repo_dir = OUTPUT_DIR / repo_name
                repo_dir.mkdir(parents=True, exist_ok=True)
                
                downloaded_path = snapshot_download(
                    repo_id=repo_id,
                    local_dir=str(repo_dir),
                    local_dir_use_symlinks=False,
                    ignore_patterns=["*.md", "*.txt", "LICENSE", ".git*", "*.ipynb"]
                )
                print(f"[Download] ✓ {repo_id} downloaded to {repo_dir}")
            except Exception as e:
                print(f"[Download] ✗ Failed to download {repo_id}: {e}")
                # Continue with other repos
                continue
        
        # Check if we got the main models
        trellis_dir = OUTPUT_DIR / "trellis-normal-v0-1"
        yoso_dir = OUTPUT_DIR / "yoso-normal-v1-8-1"
        
        if not trellis_dir.exists() and not yoso_dir.exists():
            print(f"\n[Download] ERROR: Neither trellis nor yoso models downloaded")
            return False
        
        print(f"\n[Download] Model repositories downloaded successfully")
        
    except HfHubHTTPError as e:
        if e.status_code == 401:
            print(f"[Download] ERROR: 401 Unauthorized - Repository may be private or gated")
            print(f"[Download] Solutions:")
            print(f"  1. Set HF_TOKEN environment variable with your HuggingFace token")
            print(f"  2. Get access to the repositories from Stable-X")
            return False
        elif e.status_code == 404:
            print(f"[Download] ERROR: 404 Not Found - Repository doesn't exist")
            print(f"[Download] Check if repository IDs are correct")
            return False
        else:
            print(f"[Download] ERROR: {e}")
            return False
    except Exception as e:
        print(f"[Download] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Verify we have the main models
    trellis_dir = OUTPUT_DIR / "trellis-normal-v0-1"
    yoso_dir = OUTPUT_DIR / "yoso-normal-v1-8-1"
    birefnet_dir = OUTPUT_DIR / "BiRefNet"
    
    print(f"\n[Download] Verifying downloaded models...")
    
    models_found = []
    if trellis_dir.exists():
        print(f"[Download] ✓ trellis-normal-v0-1 found")
        models_found.append("trellis")
    if yoso_dir.exists():
        print(f"[Download] ✓ yoso-normal-v1-8-1 found")
        models_found.append("yoso")
    if birefnet_dir.exists():
        print(f"[Download] ✓ BiRefNet found")
        models_found.append("birefnet")
    
    if len(models_found) == 0:
        print(f"[Download] ✗ No models downloaded")
        return False
    
    # Check for pipeline.json in one of the model dirs
    pipeline_json = None
    for model_dir in [trellis_dir, yoso_dir]:
        if model_dir.exists():
            potential_pipeline = model_dir / "pipeline.json"
            if potential_pipeline.exists():
                pipeline_json = potential_pipeline
                break
    
    if pipeline_json:
        print(f"[Download] ✓ pipeline.json found at {pipeline_json}")
    else:
        print(f"[Download] ⚠ pipeline.json not found, but models are present")
        print(f"[Download] This may be okay - Hi3DGenPipeline may construct pipeline.json from models")
    
    print(f"\n[Download] ✓ Models downloaded successfully!")
    print(f"[Download] Model directory: {OUTPUT_DIR.absolute()}")
    print(f"[Download] Downloaded: {', '.join(models_found)}")
    print(f"\n[Download] Next steps:")
    print(f"  1. Verify the Hi3DGen/ directory structure")
    print(f"  2. Update Dockerfile to uncomment: COPY Hi3DGen/ /models/hi3dgen/")
    print(f"  3. Update handler.py to use correct model path")
    print(f"  4. Build Docker image")
    return True


def download_individual_files():
    """Try downloading individual files if full repo download fails."""
    print(f"[Download] Attempting to download individual files...")
    
    # List of files we need
    files_to_download = [
        "pipeline.json",
        # Add more specific files if known
    ]
    
    for file in files_to_download:
        try:
            print(f"[Download] Downloading {file}...")
            downloaded = hf_hub_download(
                repo_id=REPO_ID,
                filename=file,
                local_dir=str(OUTPUT_DIR)
            )
            print(f"[Download] ✓ {file}")
        except Exception as e:
            print(f"[Download] ✗ Failed to download {file}: {e}")
            return False
    
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("Hi3DGen Model Download Script")
    print("=" * 60)
    print()
    
    success = download_models()
    
    if success:
        print("\n" + "=" * 60)
        print("SUCCESS: Models ready for Docker build")
        print("=" * 60)
        exit(0)
    else:
        print("\n" + "=" * 60)
        print("FAILED: Could not download models")
        print("=" * 60)
        print("\nAlternative options:")
        print("1. Get models from your existing working installation")
        print("2. Contact Microsoft for Hi3DGen model access")
        print("3. Check if repo ID needs to be different")
        exit(1)
