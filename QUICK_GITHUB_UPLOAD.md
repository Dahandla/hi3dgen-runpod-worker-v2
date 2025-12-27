# Quick GitHub Upload Checklist

## ✅ Pre-Upload Checklist

- [x] `.gitignore` created
- [ ] `hi3dgen/` and `hy3dgen/` packages included (required for imports)
- [ ] Model files handled (Git LFS or excluded)
- [ ] Dockerfile ready (use `Dockerfile.standalone` for standalone repo)

## 🚀 Quick Start Commands

```bash
# 1. Navigate to worker directory
cd hi3dgen-runpod-worker

# 2. Initialize git (if not already done)
git init

# 3. Add all files
git add .

# 4. Initial commit
git commit -m "Initial commit: Hi3DGen RunPod worker"

# 5. Create repo on GitHub (via web UI), then:
git remote add origin https://github.com/YOUR_USERNAME/hi3dgen-runpod-worker.git
git branch -M main
git push -u origin main
```

## ⚠️ Important: Package Dependencies

The worker **requires** `hi3dgen` and `hy3dgen` packages. You have two options:

### Option 1: Include in Repo (Recommended)
Copy `hi3dgen/` and `hy3dgen/` from parent directory into this repo:
```bash
# From parent directory
cp -r hi3dgen hi3dgen-runpod-worker/
cp -r hy3dgen hi3dgen-runpod-worker/
```

Then use `Dockerfile.standalone` (rename it to `Dockerfile`).

### Option 2: Use Parent as Build Context
Keep current structure and set RunPod build context to parent directory.

## 📝 RunPod Configuration

When importing from GitHub:
- **Repository**: `https://github.com/YOUR_USERNAME/hi3dgen-runpod-worker`
- **Dockerfile Path**: `Dockerfile`
- **Build Context**: `.` (root of repo)
- **GPU**: A10
- **Timeout**: 300s

## 🔐 Environment Variables (Set in RunPod)

```
S3_ENDPOINT=https://your-s3-endpoint.com
S3_KEY=your-access-key
S3_SECRET=your-secret-key
S3_BUCKET=hi3dgen-jobs
```

