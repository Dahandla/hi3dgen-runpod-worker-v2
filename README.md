# Hi3DGen RunPod Worker v2
hi3dgen_ RunPod Endpoint

Minimal worker skeleton for verifying RunPod deployments.

## Files
- `handler.py` – no-op handler proving lifecycle works
- `Dockerfile` – reproducible python:3.10-slim image
- `requirements.txt` – just `runpod`

## Run locally
```
pip install -r requirements.txt
python handler.py
```

## Deploy on RunPod
1. Create Queue endpoint, CPU worker, no model, no env vars.
2. Point to this repo.
3. After logs show `Waiting for jobs`, send a test request via `curl`.
