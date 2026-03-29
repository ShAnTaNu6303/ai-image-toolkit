"""
app/utils/image_utils.py
Shared helpers for loading, validating, and encoding images.
"""

import io
import base64
from typing import Tuple

import numpy as np
from PIL import Image
from fastapi import HTTPException, UploadFile

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/bmp", "image/tiff"}
MAX_FILE_SIZE_MB = 10


def validate_upload(file: UploadFile) -> None:
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type: {file.content_type}. "
                   f"Accepted: {', '.join(ALLOWED_TYPES)}",
        )


async def read_image_bytes(file: UploadFile) -> bytes:
    data = await file.read()
    if len(data) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum allowed size is {MAX_FILE_SIZE_MB} MB.",
        )
    return data


def bytes_to_pil(data: bytes) -> Image.Image:
    try:
        return Image.open(io.BytesIO(data))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not decode image: {exc}")


def pil_to_bytes(image: Image.Image, fmt: str = "PNG") -> bytes:
    buf = io.BytesIO()
    image.save(buf, format=fmt)
    return buf.getvalue()


def pil_to_cv2(image: Image.Image) -> np.ndarray:
    import cv2
    rgb = np.array(image.convert("RGB"))
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)


def cv2_to_pil(arr: np.ndarray) -> Image.Image:
    import cv2
    rgb = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)


def image_to_base64(image: Image.Image, fmt: str = "PNG") -> str:
    raw = pil_to_bytes(image, fmt)
    mime = "image/png" if fmt.upper() == "PNG" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(raw).decode()}"


def image_size_info(image: Image.Image) -> dict:
    return {"width": image.width, "height": image.height, "mode": image.mode}