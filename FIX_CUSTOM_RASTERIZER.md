# Fix: Custom Rasterizer Not Installed

## Problem

The error `module 'custom_rasterizer' has no attribute 'rasterize'` occurs because the `custom_rasterizer` package is not installed in the conda environment.

## Root Cause

The `custom_rasterizer` is a CUDA C++ extension that needs to be compiled and installed. It's located at:
- `hy3dgen/texgen/custom_rasterizer/`

This package must be installed in the conda environment before running the texture pipeline.

## Solution

Install the custom rasterizer in your conda environment:

```bash
# Activate your conda environment
conda activate hi3dgen-runpod

# Navigate to the custom_rasterizer directory
cd "R:\AddOnPublish\Hi3DGen_PBR_AddOn_V2\hy3dpaint\custom_rasterizer"
# OR if using the addon path:
cd "C:\Users\anyke\AppData\Roaming\Blender Foundation\Blender\4.5\scripts\addons\hi3dgenRemote_Backend\hy3dgen\texgen\custom_rasterizer"

# Install in development mode (this will compile the CUDA extension)
pip install -e .
```

**Important**: You need:
- CUDA toolkit installed
- `nvcc` (NVIDIA CUDA Compiler) in your PATH
- Visual Studio Build Tools (on Windows) or GCC (on Linux)

## Alternative: Update Setup Script

Add this to your setup process. Update `setup_conda_env.bat`:

```batch
echo.
echo Installing custom_rasterizer...
cd "%~dp0..\hy3dgen\texgen\custom_rasterizer"
conda run -n %ENV_NAME% pip install -e .
cd "%~dp0"
```

## Verification

After installation, verify it works:

```python
import custom_rasterizer
print(dir(custom_rasterizer))  # Should show 'rasterize' in the list
```

## Troubleshooting

### If compilation fails:

1. **Check CUDA is installed**:
   ```bash
   nvcc --version
   ```

2. **Check PyTorch CUDA version matches**:
   ```python
   import torch
   print(torch.version.cuda)  # Should match your CUDA toolkit
   ```

3. **On Windows**: Ensure Visual Studio Build Tools are installed with C++ support

4. **Try building manually**:
   ```bash
   python setup.py build_ext --inplace
   ```

### If import still fails:

The package might be installed but not in the Python path. Check:
```python
import sys
print(sys.path)  # Should include the custom_rasterizer location
```

## Quick Fix Script

Create a file `install_custom_rasterizer.bat`:

```batch
@echo off
echo Installing custom_rasterizer...
set ADDON_PATH=C:\Users\anyke\AppData\Roaming\Blender Foundation\Blender\4.5\scripts\addons\hi3dgenRemote_Backend
cd "%ADDON_PATH%\hy3dgen\texgen\custom_rasterizer"
conda run -n hi3dgen-runpod pip install -e .
echo.
echo Custom rasterizer installation complete!
pause
```

Run this script to install the custom rasterizer.

