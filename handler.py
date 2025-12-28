import time

import runpod


def handler(event):
    print("Job received:", event)
    return {
        "status": "success",
        "message": f"Processed: {event.get('input', {}).get('prompt', 'No prompt')}"
    }
    
if __name__ == "__main__":
    print("Starting Hi3DGen RunPod worker")
    runpod.serverless.start({"handler": handler})
