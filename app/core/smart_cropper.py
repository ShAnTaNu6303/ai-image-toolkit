"""
app/core/smart_cropper.py
Smart cropping: detect faces or salient regions and crop around them.
"""

from __future__ import annotations

import cv2
import numpy as np
from PIL import Image
from typing import Optional, Tuple, Literal

from app.utils.image_utils import pil_to_cv2, cv2_to_pil

CropMode = Literal["face", "object", "center"]

_FACE_CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"


def smart_crop(
    image: Image.Image,
    target_size: Tuple[int, int] = (512, 512),
    mode: CropMode = "face",
    padding_ratio: float = 0.25,
) -> Image.Image:
    arr = pil_to_cv2(image)

    if mode == "face":
        region = _detect_face_region(arr)
    elif mode == "object":
        region = _detect_salient_region(arr)
    else:
        region = None

    if region is None:
        cropped = _center_crop(arr, target_size)
    else:
        x, y, w, h = _expand_region(region, arr.shape, padding_ratio)
        cropped = arr[y: y + h, x: x + w]

    resized = cv2.resize(cropped, target_size, interpolation=cv2.INTER_LANCZOS4)
    return cv2_to_pil(resized)


def _detect_face_region(
    bgr: np.ndarray,
) -> Optional[Tuple[int, int, int, int]]:
    cascade = cv2.CascadeClassifier(_FACE_CASCADE_PATH)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    faces = cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )
    if len(faces) == 0:
        return None

    largest = max(faces, key=lambda f: f[2] * f[3])
    return tuple(largest)


def _detect_salient_region(
    bgr: np.ndarray,
) -> Optional[Tuple[int, int, int, int]]:
    h, w = bgr.shape[:2]
    margin_x, margin_y = int(w * 0.15), int(h * 0.15)
    rect = (margin_x, margin_y, w - 2 * margin_x, h - 2 * margin_y)

    mask = np.zeros((h, w), np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)

    try:
        cv2.grabCut(bgr, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    except cv2.error:
        return None

    fg_mask = np.where(
        (mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0
    ).astype(np.uint8)
    coords = cv2.findNonZero(fg_mask)
    if coords is None:
        return None

    x, y, bw, bh = cv2.boundingRect(coords)
    if bw < 20 or bh < 20:
        return None
    return x, y, bw, bh


def _expand_region(
    region: Tuple[int, int, int, int],
    shape: Tuple[int, int, int],
    ratio: float,
) -> Tuple[int, int, int, int]:
    x, y, w, h = region
    img_h, img_w = shape[:2]
    pad_x = int(w * ratio)
    pad_y = int(h * ratio)
    x0 = max(0, x - pad_x)
    y0 = max(0, y - pad_y)
    x1 = min(img_w, x + w + pad_x)
    y1 = min(img_h, y + h + pad_y)
    return x0, y0, x1 - x0, y1 - y0


def _center_crop(
    bgr: np.ndarray,
    target_size: Tuple[int, int],
) -> np.ndarray:
    h, w = bgr.shape[:2]
    side = min(h, w)
    x = (w - side) // 2
    y = (h - side) // 2
    return bgr[y: y + side, x: x + side]