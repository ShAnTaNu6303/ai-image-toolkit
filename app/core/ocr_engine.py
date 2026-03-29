"""
app/core/ocr_engine.py
Multilingual OCR using Tesseract via pytesseract.
Supports English, Hindi, Marathi and combinations.
"""

from __future__ import annotations

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from dataclasses import dataclass
from typing import List, Optional

import cv2
import numpy as np
from PIL import Image

from app.utils.image_utils import pil_to_cv2

SUPPORTED_LANGUAGES = {
    "eng": "English",
    "hin": "Hindi",
    "mar": "Marathi",
    "ben": "Bengali",
    "guj": "Gujarati",
    "kan": "Kannada",
    "tam": "Tamil",
    "tel": "Telugu",
    "pan": "Punjabi",
    "ori": "Odia",
    "san": "Sanskrit",
    "enm": "English (Middle)",
    "equ": "Math / Equations",
    "osd": "Orientation Detection",
    "eng+hin": "English + Hindi",
    "eng+mar": "English + Marathi",
    "eng+hin+mar": "English + Hindi + Marathi",
    "eng+ben": "English + Bengali",
    "eng+guj": "English + Gujarati",
    "eng+kan": "English + Kannada",
    "eng+tam": "English + Tamil",
    "eng+tel": "English + Telugu",
}


@dataclass
class OCRResult:
    text: str
    language: str
    word_count: int
    confidence: Optional[float]
    lines: List[str]


def extract_text(
    image: Image.Image,
    lang: str = "eng",
    preprocess: bool = True,
    psm: int = 6,
) -> OCRResult:
    if lang not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"Unsupported language: '{lang}'. "
            f"Choose from: {list(SUPPORTED_LANGUAGES.keys())}"
        )

    arr = pil_to_cv2(image)

    if preprocess:
        arr = _preprocess_for_ocr(arr)

    config = f"--psm {psm} --oem 3"
    pil_input = Image.fromarray(cv2.cvtColor(arr, cv2.COLOR_BGR2RGB))

    raw_text = pytesseract.image_to_string(pil_input, lang=lang, config=config)
    cleaned = _clean_text(raw_text)

    try:
        data = pytesseract.image_to_data(
            pil_input, lang=lang, config=config,
            output_type=pytesseract.Output.DICT,
        )
        confidences = [
            int(c) for c in data["conf"]
            if str(c).lstrip("-").isdigit() and int(c) >= 0
        ]
        avg_conf = round(sum(confidences) / len(confidences), 1) if confidences else None
    except Exception:
        avg_conf = None

    lines = [ln.strip() for ln in cleaned.splitlines() if ln.strip()]

    return OCRResult(
        text=cleaned,
        language=SUPPORTED_LANGUAGES[lang],
        word_count=len(cleaned.split()),
        confidence=avg_conf,
        lines=lines,
    )


def _preprocess_for_ocr(bgr: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((1, 1), np.uint8)
    binary = cv2.dilate(binary, kernel, iterations=1)
    return cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)


def _clean_text(raw: str) -> str:
    lines = raw.splitlines()
    cleaned = [ln.rstrip() for ln in lines]
    result: List[str] = []
    blank_count = 0
    for ln in cleaned:
        if ln == "":
            blank_count += 1
            if blank_count <= 2:
                result.append(ln)
        else:
            blank_count = 0
            result.append(ln)
    return "\n".join(result).strip()