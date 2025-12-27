"""
S3-compatible object storage upload and signed URL generation.

Handles uploading job outputs and generating presigned URLs for downloads.
"""

import os
import boto3


# Initialize S3 client (will use env vars)
s3 = boto3.client(
    "s3",
    endpoint_url=os.environ.get("S3_ENDPOINT"),
    aws_access_key_id=os.environ.get("S3_KEY"),
    aws_secret_access_key=os.environ.get("S3_SECRET")
)

BUCKET = os.environ.get("S3_BUCKET", "hi3dgen-jobs")


def upload_job(job_id, local_dir):
    """
    Upload entire job directory to S3.
    
    Args:
        job_id: Job identifier
        local_dir: Local directory containing job outputs
        
    Returns:
        str: Presigned URL to meta.json
    """
    # Upload all files recursively
    for root, _, files in os.walk(local_dir):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, local_dir)
            s3_key = f"jobs/{job_id}/{rel_path}"
            
            s3.upload_file(full_path, BUCKET, s3_key)
    
    # Return presigned URL for meta.json
    return generate_signed_url(f"jobs/{job_id}/meta.json")


def generate_signed_url(key):
    """
    Generate presigned URL for S3 object.
    
    Args:
        key: S3 object key
        
    Returns:
        str: Presigned URL (valid for 1 hour)
    """
    return s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": BUCKET,
            "Key": key
        },
        ExpiresIn=3600
    )

