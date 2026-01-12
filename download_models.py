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
REPO_ID = "microsoft/Hi3DGen"  # Try this first, may need to be adjusted
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
        # Try to download the entire repo
        print(f"[Download] Attempting to download from {REPO_ID}...")
        downloaded_path = snapshot_download(
            repo_id=REPO_ID,
            local_dir=str(OUTPUT_DIR),
            local_dir_use_symlinks=False,
            ignore_patterns=["*.md", "*.txt", "LICENSE", ".git*"]  # Skip non-essential files
        )
        print(f"[Download] Successfully downloaded to: {downloaded_path}")
        
    except HfHubHTTPError as e:
        if e.status_code == 401:
            print(f"[Download] ERROR: 401 Unauthorized - Repository may be private or gated")
            print(f"[Download] Solutions:")
            print(f"  1. Get access to {REPO_ID} from Microsoft")
            print(f"  2. Set HF_TOKEN environment variable with your HuggingFace token")
            print(f"  3. Check if the repo ID is correct (might be different)")
            return False
        elif e.status_code == 404:
            print(f"[Download] ERROR: 404 Not Found - Repository doesn't exist at {REPO_ID}")
            print(f"[Download] Trying alternative approach: downloading individual files...")
            return download_individual_files()
        else:
            print(f"[Download] ERROR: {e}")
            return False
    except Exception as e:
        print(f"[Download] ERROR: {e}")
        print(f"[Download] Trying alternative approach: downloading individual files...")
        return download_individual_files()
    
    # Verify pipeline.json exists
    pipeline_json = OUTPUT_DIR / "pipeline.json"
    if not pipeline_json.exists():
        print(f"[Download] WARNING: pipeline.json not found. Checking structure...")
        # List what we got
        for item in OUTPUT_DIR.iterdir():
            print(f"  - {item.name}")
        return False
    
    print(f"[Download] ✓ pipeline.json found")
    
    # Read pipeline.json to see what models are needed
    with open(pipeline_json, 'r') as f:
        pipeline_config = json.load(f)
    
    models_needed = pipeline_config.get('args', {}).get('models', {})
    print(f"[Download] Models required: {list(models_needed.keys())}")
    
    # Verify model files exist
    all_found = True
    for model_name, model_path in models_needed.items():
        model_json = OUTPUT_DIR / model_path / f"{Path(model_path).name}.json"
        model_safetensors = OUTPUT_DIR / model_path / f"{Path(model_path).name}.safetensors"
        
        if model_json.exists() and model_safetensors.exists():
            print(f"[Download] ✓ {model_name}: {model_path}")
        else:
            print(f"[Download] ✗ {model_name}: Missing files")
            print(f"    Expected: {model_json}")
            print(f"    Expected: {model_safetensors}")
            all_found = False
    
    if all_found:
        print(f"\n[Download] ✓ All models downloaded successfully!")
        print(f"[Download] Model directory: {OUTPUT_DIR.absolute()}")
        print(f"\n[Download] Next steps:")
        print(f"  1. Verify the Hi3DGen/ directory structure")
        print(f"  2. Update Dockerfile to uncomment: COPY Hi3DGen/ /models/hi3dgen/")
        print(f"  3. Build Docker image")
        return True
    else:
        print(f"\n[Download] ✗ Some model files are missing")
        return False


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
