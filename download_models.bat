@echo off
REM Download Hi3DGen models for RunPod worker
REM Windows batch script

echo ============================================================
echo Hi3DGen Model Download Script
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python first.
    pause
    exit /b 1
)

REM Check if huggingface_hub is installed
python -c "import huggingface_hub" >nul 2>&1
if errorlevel 1 (
    echo Installing huggingface_hub...
    pip install huggingface_hub
)

REM Set HF token if provided (optional)
if "%HF_TOKEN%"=="" (
    echo NOTE: No HF_TOKEN set. Download may fail if repo requires authentication.
    echo Set HF_TOKEN environment variable if you have a HuggingFace token.
    echo.
)

REM Run download script
python download_models.py

if errorlevel 1 (
    echo.
    echo Download failed. Check error messages above.
    pause
    exit /b 1
) else (
    echo.
    echo Download completed successfully!
    echo.
    echo Next steps:
    echo 1. Verify Hi3DGen/ directory was created
    echo 2. Update Dockerfile to uncomment: COPY Hi3DGen/ /models/hi3dgen/
    echo 3. Build Docker image
    pause
)
