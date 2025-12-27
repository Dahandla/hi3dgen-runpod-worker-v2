"""
RunPod Serverless Handler for Hi3DGen

This is the entry point that RunPod calls.
Must match the API contract validated by the Blender addon.
"""

import traceback
from utils.validation import validate_request
from pipeline.run import run_pipeline


def handler(event):
    """
    RunPod serverless handler entry point.
    
    Args:
        event: RunPod event dict with 'input' key
        
    Returns:
        dict: Response with status, job_id, and result/error
    """
    try:
        payload = validate_request(event["input"])
        result = run_pipeline(payload)

        return {
            "status": "completed",
            "job_id": result["job_id"],
            "result": {
                "meta_url": result["meta_url"],
                "expires_in": 3600
            }
        }

    except Exception as e:
        traceback.print_exc()
        return {
            "status": "failed",
            "error": {
                "code": "PIPELINE_ERROR",
                "message": str(e),
                "retryable": True
            }
        }

