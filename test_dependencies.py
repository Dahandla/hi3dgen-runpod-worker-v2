#!/usr/bin/env python3
"""
Dependency Test Script for Hi3DGen RunPod Worker

Tests all required dependencies to ensure the environment is correctly set up.
Run this after installing requirements to verify everything works.
"""

import sys
import importlib
from typing import List, Tuple

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def test_import(module_name: str, package_name: str = None, optional: bool = False) -> Tuple[bool, str]:
    """
    Test if a module can be imported.
    
    Args:
        module_name: Name of the module to import
        package_name: Display name (defaults to module_name)
        optional: If True, failure is a warning, not an error
        
    Returns:
        (success, message)
    """
    if package_name is None:
        package_name = module_name
    
    try:
        module = importlib.import_module(module_name)
        
        # Try to get version if available
        version = None
        if hasattr(module, '__version__'):
            version = module.__version__
        elif hasattr(module, 'version'):
            version = module.version
        
        if version:
            return True, f"{package_name} {version}"
        else:
            return True, f"{package_name} (imported)"
            
    except ImportError as e:
        if optional:
            return False, f"{package_name} (optional, not installed)"
        else:
            return False, f"{package_name} - {str(e)}"
    except Exception as e:
        return False, f"{package_name} - Unexpected error: {str(e)}"


def test_cuda() -> Tuple[bool, str]:
    """Test CUDA availability."""
    try:
        import torch
        if torch.cuda.is_available():
            device_count = torch.cuda.device_count()
            device_name = torch.cuda.get_device_name(0) if device_count > 0 else "Unknown"
            cuda_version = torch.version.cuda
            return True, f"CUDA {cuda_version} - {device_count} device(s) - {device_name}"
        else:
            return False, "CUDA not available (CPU only)"
    except Exception as e:
        return False, f"CUDA test failed: {str(e)}"


def main():
    """Run all dependency tests."""
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Hi3DGen RunPod Worker - Dependency Test{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    results = []
    errors = []
    warnings = []
    
    # Core PyTorch
    print(f"{BLUE}Core PyTorch:{RESET}")
    results.append(("torch", *test_import("torch")))
    results.append(("torchvision", *test_import("torchvision")))
    results.append(("torchaudio", *test_import("torchaudio")))
    cuda_ok, cuda_msg = test_cuda()
    results.append(("CUDA", cuda_ok, cuda_msg))
    print()
    
    # ML/Deep Learning
    print(f"{BLUE}ML/Deep Learning:{RESET}")
    results.append(("transformers", *test_import("transformers")))
    results.append(("diffusers", *test_import("diffusers")))
    results.append(("accelerate", *test_import("accelerate")))
    results.append(("pytorch-lightning", *test_import("pytorch_lightning")))
    results.append(("huggingface-hub", *test_import("huggingface_hub")))
    results.append(("safetensors", *test_import("safetensors")))
    print()
    
    # Scientific Computing
    print(f"{BLUE}Scientific Computing:{RESET}")
    results.append(("numpy", *test_import("numpy")))
    results.append(("scipy", *test_import("scipy")))
    results.append(("pandas", *test_import("pandas")))
    results.append(("einops", *test_import("einops")))
    print()
    
    # Computer Vision
    print(f"{BLUE}Computer Vision:{RESET}")
    results.append(("opencv-python", *test_import("cv2")))
    results.append(("imageio", *test_import("imageio")))
    results.append(("scikit-image", *test_import("skimage")))
    results.append(("rembg", *test_import("rembg")))
    results.append(("realesrgan", *test_import("realesrgan", optional=True)))  # Optional: torchvision compatibility issue
    results.append(("basicsr", *test_import("basicsr", optional=True)))  # Optional: torchvision compatibility issue
    results.append(("facexlib", *test_import("facexlib")))
    results.append(("gfpgan", *test_import("gfpgan", optional=True)))  # Optional: torchvision compatibility issue
    results.append(("Pillow", *test_import("PIL")))
    print()
    
    # 3D Mesh Processing
    print(f"{BLUE}3D Mesh Processing:{RESET}")
    results.append(("trimesh", *test_import("trimesh")))
    results.append(("pymeshlab", *test_import("pymeshlab")))
    results.append(("pygltflib", *test_import("pygltflib")))
    results.append(("xatlas", *test_import("xatlas")))
    results.append(("open3d", *test_import("open3d")))
    print()
    
    # Configuration
    print(f"{BLUE}Configuration:{RESET}")
    results.append(("omegaconf", *test_import("omegaconf")))
    results.append(("pyyaml", *test_import("yaml")))
    results.append(("configargparse", *test_import("configargparse")))
    print()
    
    # Build Tools
    print(f"{BLUE}Build Tools:{RESET}")
    results.append(("ninja", *test_import("ninja")))
    results.append(("pybind11", *test_import("pybind11")))
    print()
    
    # GPU Computing
    print(f"{BLUE}GPU Computing:{RESET}")
    results.append(("cupy", *test_import("cupy", optional=True)))
    print()
    
    # Additional ML
    print(f"{BLUE}Additional ML:{RESET}")
    results.append(("kornia", *test_import("kornia")))
    results.append(("timm", *test_import("timm")))
    results.append(("torchdiffeq", *test_import("torchdiffeq")))
    print()
    
    # Utilities
    print(f"{BLUE}Utilities:{RESET}")
    results.append(("tqdm", *test_import("tqdm")))
    results.append(("psutil", *test_import("psutil")))
    results.append(("pydantic", *test_import("pydantic")))
    print()
    
    # Cloud Storage
    print(f"{BLUE}Cloud Storage:{RESET}")
    results.append(("boto3", *test_import("boto3")))
    results.append(("requests", *test_import("requests")))
    print()
    
    # Optional Dependencies
    print(f"{BLUE}Optional Dependencies:{RESET}")
    results.append(("spconv", *test_import("spconv", optional=True)))
    results.append(("xformers", *test_import("xformers", optional=True)))
    results.append(("onnxruntime", *test_import("onnxruntime", optional=True)))
    results.append(("torchmetrics", *test_import("torchmetrics", optional=True)))
    print()
    
    # Print Results
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Test Results:{RESET}\n")
    
    for name, success, message in results:
        if success:
            print(f"{GREEN}✓{RESET} {name:25} - {message}")
        else:
            if "optional" in message.lower():
                print(f"{YELLOW}⚠{RESET} {name:25} - {message}")
                warnings.append(name)
            else:
                print(f"{RED}✗{RESET} {name:25} - {message}")
                errors.append(name)
    
    print()
    print(f"{BLUE}{'='*60}{RESET}")
    
    # Summary
    total = len(results)
    passed = total - len(errors) - len(warnings)
    failed = len(errors)
    optional_missing = len(warnings)
    
    print(f"\n{BLUE}Summary:{RESET}")
    print(f"  {GREEN}Passed:{RESET} {passed}/{total}")
    if warnings:
        print(f"  {YELLOW}Optional Missing:{RESET} {optional_missing}")
    if errors:
        print(f"  {RED}Failed:{RESET} {failed}")
    
    print()
    
    if errors:
        print(f"{RED}❌ Some required dependencies are missing!{RESET}")
        print(f"{RED}Please install the missing packages before deployment.{RESET}\n")
        sys.exit(1)
    elif warnings:
        print(f"{YELLOW}⚠ Some optional dependencies are missing.{RESET}")
        print(f"{YELLOW}This is OK, but some features may not work optimally.{RESET}\n")
        print(f"{GREEN}✓ All required dependencies are installed!{RESET}\n")
        sys.exit(0)
    else:
        print(f"{GREEN}✓ All dependencies are installed correctly!{RESET}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()

