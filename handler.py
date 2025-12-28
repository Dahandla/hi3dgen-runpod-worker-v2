import runpod
import time

def handler(event):
    print("Job received:", event)

    # Simulate processing time
    time.sleep(2)

    # Fake but valid Hi3DGen-style payload
    return {
        "status": "completed",
        "result": {
            "mesh": "placeholder.glb",
            "textures": [],
            "meta": {
                "generator": "hi3dgen-runpod-worker-v2"
            }
        },
        "message": "Successfully processed job"
    }
    
if __name__ == "__main__":
    print("Starting Hi3DGen RunPod worker")
    runpod.serverless.start({"handler": handler})
