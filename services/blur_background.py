# --- blur_background.py ---
from typing import Dict, Any, Optional
import requests
import base64

def blur_background(
    api_key: str,
    image_data: bytes = None,
    image_url: Optional[str] = None,
    scale: int = 5,
    force_rmbg: bool = False,
    content_moderation: bool = False
) -> Dict[str, Any]:
    """
    Blur the background of an image.

    Args:
        api_key: Bria API key
        image_data: Image in bytes (used if image_url is not provided)
        image_url: URL of the image (used if provided)
        scale: Blur intensity (1 to 5)
        force_rmbg: Force background removal
        content_moderation: Enable content moderation

    Returns:
        API response JSON
    """
    url = "https://engine.prod.bria-api.com/v1/background/blur"

    headers = {
        "Content-Type": "application/json",
        "api_token": api_key
    }

    payload = {
        "scale": max(1, min(scale, 5)),
        "force_rmbg": force_rmbg,
        "content_moderation": content_moderation
    }

    if image_url:
        payload["image_url"] = image_url
    elif image_data:
        payload["file"] = base64.b64encode(image_data).decode("utf-8")
    else:
        raise ValueError("Either image_url or image_data must be provided")

    try:
        print(f"Requesting {url} with payload: {payload}")
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise Exception(f"Blur background failed: {str(e)}")
    