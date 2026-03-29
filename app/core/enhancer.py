"""
app/core/enhancer.py
Image quality enhancement: denoising, brightness/contrast adjustment.
"""

from dataclasses import dataclass
from typing import Optional

import cv2
import numpy as np
from PIL import Image

from app.utils.image_utils import pil_to_cv2, cv2_to_pil


@dataclass
class EnhancementConfig:
    denoise: bool = True
    denoise_h: float = 10.0
    brightness: int = 0
    contrast: float = 1.0
    sharpen: bool = False
    auto_white_balance: bool = False


def enhance_image(
    image: Image.Image,
    config: Optional[EnhancementConfig] = None,
) -> Image.Image:
    if config is None:
        config = EnhancementConfig()

    arr = pil_to_cv2(image)

    if config.auto_white_balance:
        arr = _auto_white_balance(arr)

    if config.denoise:
        arr = cv2.fastNlMeansDenoisingColored(
            arr,
            None,
            h=config.denoise_h,
            hColor=config.denoise_h,
            templateWindowSize=7,
            searchWindowSize=21,
        )

    if config.brightness != 0 or config.contrast != 1.0:
        arr = cv2.convertScaleAbs(
            arr,
            alpha=config.contrast,
            beta=config.brightness,
        )

    if config.sharpen:
        arr = _unsharp_mask(arr)

    return cv2_to_pil(arr)


def _auto_white_balance(bgr: np.ndarray) -> np.ndarray:
    result = np.zeros_like(bgr)
    for i in range(3):
        ch = bgr[:, :, i].astype(np.float32)
        lo, hi = ch.min(), ch.max()
        if hi > lo:
            result[:, :, i] = np.clip((ch - lo) / (hi - lo) * 255, 0, 255).astype(np.uint8)
        else:
            result[:, :, i] = bgr[:, :, i]
    return result


def _unsharp_mask(
    bgr: np.ndarray,
    kernel_size: int = 5,
    sigma: float = 1.0,
    amount: float = 1.0,
    threshold: int = 0,
) -> np.ndarray:
    blurred = cv2.GaussianBlur(bgr, (kernel_size, kernel_size), sigma)
    sharpened = cv2.addWeighted(bgr, 1 + amount, blurred, -amount, 0)
    if threshold > 0:
        low_contrast = np.abs(bgr.astype(int) - blurred.astype(int)) < threshold
        sharpened[low_contrast] = bgr[low_contrast]
    return sharpened