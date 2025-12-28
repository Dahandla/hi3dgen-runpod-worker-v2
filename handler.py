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
            "echo_input": event.get("input", {}),
            "job_id": job_id,
            "server_time_utc": now,
            "marker": marker,
        }
    }

if __name__ == "__main__":
    print("Starting Hi3DGen RunPod worker (VISIBLE OUTPUT MODE)")
    runpod.serverless.start({"handler": handler})
