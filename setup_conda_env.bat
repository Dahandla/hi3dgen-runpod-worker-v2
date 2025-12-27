@echo off
REM Setup script for Hi3DGen RunPod Worker Conda Environment (Windows)
REM Run this script to set up a complete development environment

set ENV_NAME=hi3dgen-runpod
set PYTHON_VERSION=3.10

echo ==========================================
echo Hi3DGen RunPod Worker - Environment Setup
echo ==========================================
echo.

REM Check if conda is installed
where conda >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: conda is not installed or not in PATH
    echo Please install Miniconda first: https://docs.conda.io/en/latest/miniconda.html
    exit /b 1
)

REM Check if environment already exists
conda env list | findstr /C:"%ENV_NAME%" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Environment '%ENV_NAME%' already exists.
    set /p REMOVE_ENV="Do you want to remove it and create a new one? (y/N): "
    if /i "%REMOVE_ENV%"=="y" (
        echo Removing existing environment...
        conda env remove -n %ENV_NAME% -y
    ) else (
        echo Using existing environment. Activate it with: conda activate %ENV_NAME%
        exit /b 0
    )
)

REM Create conda environment
echo Creating conda environment '%ENV_NAME%' with Python %PYTHON_VERSION%...
conda create -n %ENV_NAME% python=%PYTHON_VERSION% -y
if %ERRORLEVEL% NEQ 0 (
    echo Failed to create conda environment
    exit /b 1
)

REM Use conda run to execute commands in the environment
echo Activating environment and installing packages...
echo.

echo Installing PyTorch with CUDA 12.4...
conda run -n %ENV_NAME% pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124
if %ERRORLEVEL% NEQ 0 (
    echo Warning: PyTorch installation may have failed
)

echo.
echo Installing spconv (CUDA 12.0)...
conda run -n %ENV_NAME% pip install spconv-cu120==2.3.6
if %ERRORLEVEL% NEQ 0 (
    echo Warning: spconv installation may have failed
)

echo.
echo Installing xformers...
conda run -n %ENV_NAME% pip install -U xformers --index-url https://download.pytorch.org/whl/cu124
if %ERRORLEVEL% NEQ 0 (
    echo Warning: xformers installation may have failed
)

echo.
echo Installing other requirements...
conda run -n %ENV_NAME% pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Some requirements may have failed to install
)

echo.
echo Testing dependencies...
conda run -n %ENV_NAME% python test_dependencies.py

echo.
echo ==========================================
echo Setup complete!
echo ==========================================
echo.
echo To activate the environment, run:
echo   conda activate %ENV_NAME%
echo.
echo To test dependencies again, run:
echo   python test_dependencies.py
echo.

pause

