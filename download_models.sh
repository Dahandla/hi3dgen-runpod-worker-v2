#!/bin/bash
# Download Hi3DGen models for RunPod worker
# Linux/Mac shell script

echo "============================================================"
echo "Hi3DGen Model Download Script"
echo "============================================================"
echo

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "ERROR: Python not found. Please install Python first."
    exit 1
fi

# Check if huggingface_hub is installed
python -c "import huggingface_hub" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing huggingface_hub..."
    pip install huggingface_hub
fi

# Check for HF token
if [ -z "$HF_TOKEN" ] && [ -z "$HUGGINGFACE_TOKEN" ]; then
    echo "NOTE: No HF_TOKEN set. Download may fail if repo requires authentication."
    echo "Set HF_TOKEN environment variable if you have a HuggingFace token."
    echo
fi

# Run download script
python download_models.py

if [ $? -ne 0 ]; then
    echo
    echo "Download failed. Check error messages above."
    exit 1
else
    echo
    echo "Download completed successfully!"
    echo
    echo "Next steps:"
    echo "1. Verify Hi3DGen/ directory was created"
    echo "2. Update Dockerfile to uncomment: COPY Hi3DGen/ /models/hi3dgen/"
    echo "3. Build Docker image"
fi
