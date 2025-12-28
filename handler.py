import time

import runpod


def handler(event):
    print("Job received:", event)
    time.sleep(2)

    return {
        "status": "ok",
        "message": "Hi3DGen worker is alive"
    }


if __name__ == "__main__":
    print("Starting Hi3DGen RunPod worker")
    runpod.serverless.start({"handler": handler})
