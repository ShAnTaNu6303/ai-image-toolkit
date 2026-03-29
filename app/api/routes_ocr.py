"""
app/api/routes_ocr.py
API route: POST /api/ocr/extract
"""

from fastapi import APIRouter, UploadFile, File, Query
from fastapi.responses import JSONResponse

from app.core.ocr_engine import extract_text, SUPPORTED_LANGUAGES
from app.utils.image_utils import (
    validate_upload,
    read_image_bytes,
    bytes_to_pil,
    image_size_info,
)

router = APIRouter()


@router.post(
    "/extract",
    summary="Extract text from image (multilingual OCR)",
    response_description="JSON with extracted text, word count, and confidence",
)
async def ocr_extract(
    file: UploadFile = File(...),
    lang: str = Query(
        "eng",
        description="Language code: eng, hin, mar, eng+hin, eng+mar, eng+hin+mar",
    ),
    preprocess: bool = Query(True, description="Apply image preprocessing before OCR"),
    psm: int = Query(6, ge=0, le=13, description="Tesseract page segmentation mode (0-13)"),
):
    validate_upload(file)
    raw = await read_image_bytes(file)
    image = bytes_to_pil(raw)

    result = extract_text(image, lang=lang, preprocess=preprocess, psm=psm)

    return JSONResponse({
        "text": result.text,
        "lines": result.lines,
        "language": result.language,
        "word_count": result.word_count,
        "avg_confidence": result.confidence,
        "image_info": image_size_info(image),
    })


@router.get(
    "/languages",
    summary="List supported OCR languages",
)
def list_languages():
    return {"supported_languages": SUPPORTED_LANGUAGES}