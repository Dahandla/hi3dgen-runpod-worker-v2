# Minimal Dummy Worker Setup

This is a minimal RunPod serverless worker that creates a simple cube and returns it as base64-encoded GLB. Use this to verify the RunPod serverless lifecycle before integrating real Hi3DGen logic.

## Files

- `handler.py` - Creates a cube, exports to GLB, returns base64
- `Dockerfile` - Minimal Python 3.10 image
- `requirements.txt` - Only trimesh, runpod, numpy

## Build & Deploy

### 1. Build Docker Image

```bash
cd hi3dgen-runpod-worker
docker build -t yourname/hi3dgen-dummy:glbtest-v1 .
```

**⚠️ IMPORTANT: Use a NEW tag name every time (v1, v2, etc.)**

### 2. Push to Registry

```bash
docker push yourname/hi3dgen-dummy:glbtest-v1
```

### 3. Create NEW RunPod Serverless Endpoint

**⚠️ CRITICAL: You MUST create a NEW endpoint. Updating the old one does NOT work.**

1. Go to RunPod Dashboard → Serverless
2. Click "Create Endpoint"
3. Choose "Custom Docker Image"
4. Set:
   - **Container image**: `yourname/hi3dgen-dummy:glbtest-v1`
   - **GPU**: CPU is fine for dummy (or any GPU type)
   - **Name**: `hi3dgen-dummy-test` (or any name)
5. Click "Create"
6. Copy the NEW endpoint ID

### 4. Configure Blender Addon

1. Open Blender addon preferences
2. Set **RunPod Connection Type** to "API"
3. Set **Remote Server URL** to: `https://api.runpod.ai/v2/<NEW_ENDPOINT_ID>`
4. Set **RunPod API Key** (optional but recommended)

### 5. Test

1. In Blender, use the Hi3DGen addon to generate a mesh
2. You should see a unit cube imported into Blender
3. Check console for debug output showing vertices/faces count

## Success Criteria

When this works, you will see:
- ✅ A unit cube imported into Blender
- ✅ Correct scale (1x1x1)
- ✅ No materials (expected for dummy)
- ✅ No textures (expected for dummy)
- ✅ Debug print shows vertices/faces count

## Next Steps

Once the cube imports correctly:
1. Replace cube with real Hi3DGen mesh output
2. Add UVs and dummy PBR material
3. Integrate real Hi3DGen pipeline
4. Add texture baking / PBR maps

## Troubleshooting

### Still getting "worker is alive" message
- You're hitting the OLD endpoint
- Create a NEW endpoint with a NEW image tag
- Update Blender addon URL to the NEW endpoint ID

### No mesh imported
- Check Blender console for errors
- Verify endpoint URL is correct
- Check RunPod endpoint logs for handler errors

### Handler errors
- Check RunPod endpoint logs
- Verify Docker image was pushed correctly
- Ensure handler.py is in the image
