import requests
import base64
from typing import Optional, Dict, Any

def enhance_image(
    api_key: str,
    image_data: Optional[bytes] = None,
    image_url: Optional[str] = None,
    content_moderation: bool = False,
    resolution: str = "2MP",
    seed: Optional[int] = None,
    steps_num: int = 20,
    sync: bool = True
) -> Dict[str, Any]:
    """
    Enhance the visual quality of an image using Bria's /enhance_image API.

    Args:
        api_key: Bria API key.
        image_data: Image in bytes (used if image_url is not provided).
        image_url: URL of the image (used if provided).
        content_moderation: Whether to enable content moderation.
        resolution: Target output resolution ("1MP", "2MP", "4MP").
        seed: Optional seed to control generation randomness.
        steps_num: Number of enhancement steps (10–50).
        sync: Whether to make the request synchronous.

    Returns:
        API response JSON.
    """
    url = "https://engine.prod.bria-api.com/v1/enhance_image"

    headers = {
        "Content-Type": "application/json",
        "api_token": api_key
    }

    payload = {
        "content_moderation": content_moderation,
        "resolution": resolution,
        "steps_num": max(10, min(steps_num, 50)),
        "sync": sync
    }

    if image_url:
        payload["image_url"] = image_url
    elif image_data:
        payload["image_file"] = base64.b64encode(image_data).decode("utf-8")
    else:
        raise ValueError("Either image_url or image_data must be provided.")

    if seed is not None:
        payload["seed"] = seed

    try:
        print("Sending payload to /enhance_image:", payload)
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        raise Exception(f"HTTP error: {http_err.response.status_code} - {http_err.response.text}")
    except Exception as err:
        raise Exception(f"Enhance image failed: {str(err)}")
