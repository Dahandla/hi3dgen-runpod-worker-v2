"""
Progress tracking utilities.

Can be extended to send progress updates to RunPod or external systems.
"""


def log_progress(stage, progress_pct, message=""):
    """
    Log pipeline progress.
    
    Args:
        stage: Current pipeline stage (e.g., "multiview", "mesh", "texture")
        progress_pct: Progress percentage (0-100)
        message: Optional status message
    """
    # TODO: Integrate with RunPod progress API if needed
    print(f"[Progress] {stage}: {progress_pct}% - {message}")

