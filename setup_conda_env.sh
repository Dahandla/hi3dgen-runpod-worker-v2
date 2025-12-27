#!/bin/bash
# Setup script for Hi3DGen RunPod Worker Conda Environment
# Run this script to set up a complete development environment

set -e  # Exit on error

ENV_NAME="hi3dgen-runpod"
PYTHON_VERSION="3.10"

echo "=========================================="
echo "Hi3DGen RunPod Worker - Environment Setup"
echo "=========================================="
echo ""

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "Error: conda is not installed or not in PATH"
    echo "Please install Miniconda first: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# Check if environment already exists
if conda env list | grep -q "^${ENV_NAME} "; then
    echo "Environment '${ENV_NAME}' already exists."
    read -p "Do you want to remove it and create a new one? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing existing environment..."
        conda env remove -n ${ENV_NAME} -y
    else
        echo "Using existing environment. Activate it with: conda activate ${ENV_NAME}"
        exit 0
    fi
fi

# Create conda environment
echo "Creating conda environment '${ENV_NAME}' with Python ${PYTHON_VERSION}..."
conda create -n ${ENV_NAME} python=${PYTHON_VERSION} -y

# Activate environment
echo "Activating environment..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate ${ENV_NAME}

# Install PyTorch with CUDA 12.4
echo ""
echo "Installing PyTorch with CUDA 12.4..."
pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124

# Install spconv
echo ""
echo "Installing spconv (CUDA 12.0)..."
pip install spconv-cu120==2.3.6

# Install xformers
echo ""
echo "Installing xformers..."
pip install -U xformers --index-url https://download.pytorch.org/whl/cu124

# Install other requirements
echo ""
echo "Installing other requirements..."
pip install -r requirements.txt

# Test dependencies
echo ""
echo "Testing dependencies..."
python test_dependencies.py

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "To activate the environment, run:"
echo "  conda activate ${ENV_NAME}"
echo ""
echo "To test dependencies again, run:"
echo "  python test_dependencies.py"
echo ""

