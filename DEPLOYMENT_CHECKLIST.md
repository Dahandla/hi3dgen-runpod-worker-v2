# Hi3DGen RunPod Worker - Deployment Checklist

Complete step-by-step checklist for deploying the Hi3DGen RunPod serverless worker.

## Pre-Deployment Checklist

### ✅ 1. Code Structure
- [x] Handler (`handler.py`) is implemented
- [x] Pipeline modules exist (`pipeline/run.py`, `multiview.py`, `mesh.py`, `texture.py`, `export.py`)
- [x] Utils modules exist (`utils/validation.py`, `utils/storage.py`, `utils/progress.py`)
- [x] Dockerfile is configured
- [x] Requirements.txt is complete
- [ ] **Pipeline implementations are complete** (currently placeholders)
- [ ] **Model weights are added** to `models/` directory

### ✅ 2. Model Weights
- [ ] Add Hi3DGen model weights to `models/hi3dgen/`
- [ ] Add Zero123 model weights to `models/zero123/` (if needed)
- [ ] Verify model file paths match your pipeline code
- [ ] Test model loading locally before Docker build

### ✅ 3. Pipeline Implementation
- [ ] Implement `pipeline/multiview.py` - Replace placeholder with actual Zero123/Hi3DGen multiview generation
- [ ] Implement `pipeline/mesh.py` - Replace placeholder with actual Hi3DGen mesh generation
- [ ] Implement `pipeline/texture.py` - Replace placeholder with actual texture baking code
- [ ] Test each pipeline stage locally
- [ ] Verify outputs match expected format (GLB mesh, PNG textures)

### ✅ 4. Environment Variables
Prepare these for RunPod endpoint configuration:
- [ ] `S3_ENDPOINT` - Your S3-compatible storage endpoint URL
- [ ] `S3_KEY` - Access key ID
- [ ] `S3_SECRET` - Secret access key
- [ ] `S3_BUCKET` - Bucket name (e.g., "hi3dgen-jobs")

### ✅ 5. S3 Storage Setup
- [ ] Create S3 bucket (or RunPod Object Storage bucket)
- [ ] Configure bucket permissions (read/write)
- [ ] Test S3 credentials locally
- [ ] Verify presigned URL generation works

## Docker Build Checklist

### ✅ 6. Local Testing
- [ ] Test Docker build locally: `docker build -t hi3dgen-runpod-worker:latest .`
- [ ] Verify build completes without errors
- [ ] Check that custom_rasterizer compiles successfully
- [ ] Check that differentiable_renderer compiles successfully
- [ ] Test handler import: `docker run --rm hi3dgen-runpod-worker:latest python3 -c "from handler import handler; print('OK')"`

### ✅ 7. Docker Image Size
- [ ] Check image size (should be reasonable, <10GB if possible)
- [ ] Consider multi-stage build if size is too large
- [ ] Verify models are included in image

### ✅ 8. Registry Push
- [ ] Tag image: `docker tag hi3dgen-runpod-worker:latest your-registry/hi3dgen-runpod-worker:latest`
- [ ] Push to registry: `docker push your-registry/hi3dgen-runpod-worker:latest`
- [ ] Verify image is accessible from RunPod

## RunPod Deployment Checklist

### ✅ 9. Create Serverless Endpoint
- [ ] Log into RunPod console
- [ ] Navigate to Serverless → Endpoints
- [ ] Click "Create Endpoint"
- [ ] Configure:
  - [ ] **Name**: `hi3dgen-worker`
  - [ ] **GPU Type**: A10 (or your preferred GPU)
  - [ ] **Container Image**: `your-registry/hi3dgen-runpod-worker:latest`
  - [ ] **Timeout**: 300 seconds (5 minutes)
  - [ ] **Max Workers**: Set based on expected load
  - [ ] **Flashboot**: Enabled (faster cold starts)

### ✅ 10. Environment Variables
Set in RunPod endpoint configuration:
- [ ] `S3_ENDPOINT` = `https://your-s3-endpoint.com`
- [ ] `S3_KEY` = `your-access-key`
- [ ] `S3_SECRET` = `your-secret-key`
- [ ] `S3_BUCKET` = `hi3dgen-jobs`
- [ ] `PYTHONUNBUFFERED` = `1` (optional, for better logging)

### ✅ 11. Test Endpoint
- [ ] Get endpoint URL from RunPod console
- [ ] Test with simple request:
  ```json
  {
    "api_version": "1.0",
    "input": {
      "image_url": "https://example.com/test-image.jpg"
    }
  }
  ```
- [ ] Verify response format matches expected contract
- [ ] Check RunPod logs for errors

## Blender Addon Integration Checklist

### ✅ 12. Configure Blender Addon
- [ ] Open Blender addon preferences
- [ ] Set backend to "REMOTE"
- [ ] Paste RunPod endpoint URL
- [ ] Test connection (if addon supports it)

### ✅ 13. End-to-End Test
- [ ] Submit a job from Blender addon
- [ ] Verify job is accepted by RunPod
- [ ] Monitor job progress in RunPod console
- [ ] Verify outputs are uploaded to S3
- [ ] Verify Blender addon downloads results
- [ ] Verify mesh and textures import correctly

## Post-Deployment Checklist

### ✅ 14. Monitoring
- [ ] Set up RunPod monitoring/alerts
- [ ] Monitor S3 storage usage
- [ ] Track job success/failure rates
- [ ] Monitor average job duration
- [ ] Set up cost alerts

### ✅ 15. Optimization
- [ ] Review job execution times
- [ ] Adjust timeout if needed
- [ ] Optimize model loading (preload if possible)
- [ ] Consider caching frequently used models
- [ ] Review and optimize Docker image size

### ✅ 16. Documentation
- [ ] Document endpoint URL for team
- [ ] Document S3 credentials (securely)
- [ ] Document any custom configuration
- [ ] Update README with deployment notes

## Troubleshooting Checklist

If deployment fails, check:

### Build Issues
- [ ] Verify CUDA toolkit version matches base image
- [ ] Check custom_rasterizer compilation logs
- [ ] Verify all dependencies are in requirements.txt
- [ ] Check Docker build logs for errors

### Runtime Issues
- [ ] Check RunPod worker logs
- [ ] Verify environment variables are set correctly
- [ ] Test S3 connectivity from worker
- [ ] Verify model paths are correct
- [ ] Check GPU memory usage

### API Issues
- [ ] Verify handler function signature matches RunPod format
- [ ] Check request validation logic
- [ ] Verify response format matches Blender addon expectations
- [ ] Test with curl/Postman if addon has issues

## Quick Reference

### Docker Build Command
```bash
# From the project root directory (parent of hi3dgen-runpod-worker/)
docker build -f hi3dgen-runpod-worker/Dockerfile -t hi3dgen-runpod-worker:latest .
```

### Docker Test Command
```bash
docker run --rm \
  -e S3_ENDPOINT=https://your-endpoint.com \
  -e S3_KEY=your-key \
  -e S3_SECRET=your-secret \
  -e S3_BUCKET=hi3dgen-jobs \
  hi3dgen-runpod-worker:latest \
  python3 -c "from handler import handler; print('Handler ready')"
```

### Test Request Format
```json
{
  "api_version": "1.0",
  "input": {
    "image_url": "https://example.com/image.jpg"
  }
}
```

### Expected Response Format
```json
{
  "status": "completed",
  "job_id": "job_xxxxxxxx",
  "result": {
    "meta_url": "https://s3.../jobs/job_xxx/meta.json",
    "expires_in": 3600
  }
}
```

## Notes

- **Pipeline Placeholders**: Remember to implement actual model inference in `multiview.py`, `mesh.py`, and `texture.py` before production use
- **Model Weights**: Must be added to `models/` directory before building Docker image
- **Custom Extensions**: Custom rasterizer and differentiable renderer are now included in Dockerfile
- **S3 Storage**: All outputs are uploaded to S3, no local storage on workers
- **Timeout**: Default 180s runtime cap can be adjusted in `pipeline/run.py`

## Support

If you encounter issues:
1. Check RunPod worker logs in console
2. Review Docker build logs
3. Test components individually (handler, pipeline stages)
4. Verify S3 credentials and connectivity
5. Check model file paths and formats

