# GitHub Setup Guide

This guide will help you prepare and upload the `hi3dgen-runpod-worker` to GitHub for RunPod deployment.

## Prerequisites

- Git installed
- GitHub account
- Access to the `hi3dgen` and `hy3dgen` packages (they need to be included in the repo)

## Step 1: Decide on Repository Structure

You have two options:

### Option A: Standalone Repository (Recommended)

Include `hi3dgen` and `hy3dgen` packages directly in the repository. This makes it self-contained.

**Structure:**
```
hi3dgen-runpod-worker/
├── Dockerfile (use Dockerfile.standalone)
├── requirements.txt
├── handler.py
├── pipeline/
├── utils/
├── models/
├── hi3dgen/          ← Include this
├── hy3dgen/          ← Include this
└── README.md
```

### Option B: Parent Directory as Build Context

Keep the current structure and use the parent directory as Docker build context.

**Structure:**
```
parent-repo/
├── hi3dgen-runpod-worker/
│   ├── Dockerfile (current version)
│   ├── requirements.txt
│   ├── handler.py
│   ├── pipeline/
│   ├── utils/
│   └── models/
├── hi3dgen/
└── hy3dgen/
```

## Step 2: Initialize Git Repository

```bash
cd hi3dgen-runpod-worker

# Initialize git
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: Hi3DGen RunPod worker"
```

## Step 3: Handle Large Model Files

If you have large model files in `models/`, use Git LFS:

```bash
# Install Git LFS (if not already installed)
git lfs install

# Track large files
git lfs track "models/**/*.safetensors"
git lfs track "models/**/*.pt"
git lfs track "models/**/*.pth"
git lfs track "models/**/*.ckpt"

# Add .gitattributes
git add .gitattributes
git commit -m "Add Git LFS tracking for model files"
```

**Note**: If models are not included (they'll be downloaded at runtime), you can skip this step.

## Step 4: Create GitHub Repository

1. Go to GitHub and create a new repository named `hi3dgen-runpod-worker`
2. **Do NOT** initialize with README, .gitignore, or license (we already have these)

## Step 5: Push to GitHub

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/hi3dgen-runpod-worker.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 6: Configure RunPod

1. Go to RunPod → Deploy Serverless Endpoint
2. Select **"Import GitHub Repository"**
3. Enter your repository URL: `https://github.com/YOUR_USERNAME/hi3dgen-runpod-worker`
4. Configure:
   - **Dockerfile Path**: `Dockerfile` (or `Dockerfile.standalone` if using Option A)
   - **Build Context**: 
     - Option A: `.` (root of repo)
     - Option B: `..` (parent directory)
   - **GPU**: A10 or your preferred GPU
   - **Timeout**: 300s (5 minutes)

## Step 7: Set Environment Variables

In RunPod endpoint configuration, set:

```
S3_ENDPOINT=https://your-s3-endpoint.com
S3_KEY=your-access-key
S3_SECRET=your-secret-key
S3_BUCKET=hi3dgen-jobs
```

## Troubleshooting

### Build Fails: Cannot find hi3dgen/hy3dgen

- **Solution**: Make sure `hi3dgen` and `hy3dgen` are included in the repository
- Or adjust Dockerfile paths to match your structure

### Build Fails: Custom rasterizer compilation error

- This is expected if CUDA toolkit version doesn't match
- The Dockerfile includes `|| echo "Warning..."` to continue on failure
- Check RunPod logs for specific errors

### Models Not Found

- Ensure models are in `models/` directory
- Or configure model download in your pipeline code
- Consider using Git LFS for large model files

## Next Steps

After successful deployment:

1. Test with your Blender addon
2. Monitor RunPod logs for any issues
3. Adjust timeout/GPU settings as needed
4. Set up CI/CD for automatic redeployment on push (optional)

