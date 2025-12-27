# Torchvision Compatibility Fix

## Issue

The packages `realesrgan`, `basicsr`, and `gfpgan` fail to import with torchvision 0.21.0 due to missing `torchvision.transforms.functional_tensor`.

Error:
```
No module named 'torchvision.transforms.functional_tensor'
```

## Root Cause

These packages depend on `torchvision.transforms.functional_tensor` which was removed or renamed in newer versions of torchvision. The API changed between torchvision versions.

## Solution Options

### Option 1: Mark as Optional (Recommended)

These packages are for image enhancement/super-resolution, not core to the 3D generation pipeline. They've been marked as optional in:
- `requirements.txt` (commented out)
- `test_dependencies.py` (marked as optional)

**Status**: ✅ Already implemented

### Option 2: Use Compatible Versions

If you need these packages, you can try:

1. **Downgrade torchvision** (not recommended - breaks other dependencies):
   ```bash
   pip install torchvision==0.20.0
   ```

2. **Use alternative packages**:
   - For super-resolution: Use `realesrgan-ncnn-py` or other alternatives
   - For face enhancement: Use updated versions that support newer torchvision

3. **Patch the packages** (advanced):
   - Fork and update the packages to use the new torchvision API
   - Or use monkey-patching to redirect imports

### Option 3: Skip for RunPod Worker

For the RunPod worker, these image enhancement features may not be necessary:
- The core 3D generation pipeline doesn't require them
- They add significant dependencies and build complexity
- Image enhancement can be done client-side in Blender if needed

## Current Status

✅ **realesrgan** - Marked as optional  
✅ **basicsr** - Marked as optional  
✅ **gfpgan** - Marked as optional  
✅ **facexlib** - Working (no issues)  
✅ **rembg** - Working (no issues)  

## Testing

Run the dependency test:

```bash
python test_dependencies.py
```

The test will show these as optional warnings (⚠) rather than errors (✗), and the test will pass.

## For Production

If you need image enhancement features:

1. **Client-side**: Do enhancement in Blender before sending to server
2. **Separate service**: Run enhancement as a separate microservice
3. **Alternative libraries**: Use torchvision-compatible alternatives
4. **Custom implementation**: Implement enhancement using working libraries (opencv, PIL, etc.)

## References

- [torchvision transforms documentation](https://pytorch.org/vision/stable/transforms.html)
- [realesrgan GitHub](https://github.com/xinntao/Real-ESRGAN)
- [basicsr GitHub](https://github.com/xinntao/BasicSR)
- [gfpgan GitHub](https://github.com/TencentARC/GFPGAN)

