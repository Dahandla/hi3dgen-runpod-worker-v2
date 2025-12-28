import runpod
import time
import uuid
import datetime

def handler(event):
    job_id = event.get("id", "unknown")
    marker = str(uuid.uuid4())[:8]
    now = datetime.datetime.utcnow().isoformat()

    print(f"[Hi3DGen] Job received: {job_id}")
    print(f"[Hi3DGen] Marker: {marker}")

    time.sleep(1)

    return {
        "status": "completed",
        "result": {
            "marker": marker,
            "server_time_utc": now,
            "message": "Visible test payload from RunPod worker",
            "echo_input": event.get("input", {})
        }
    }

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
