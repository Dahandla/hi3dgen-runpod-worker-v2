"""
Request validation for API contract enforcement.
"""


def validate_request(data):
    """
    Validate incoming request payload.
    
    Args:
        data: Request payload dict
        
    Returns:
        dict: Validated payload
        
    Raises:
        ValueError: If validation fails
    """
    if data.get("api_version") != "1.0":
        raise ValueError("Unsupported API version")
    
    if "input" not in data or "image_url" not in data["input"]:
        raise ValueError("Missing image_url")
    
    return data

