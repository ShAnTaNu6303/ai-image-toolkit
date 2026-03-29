"""
app/api/routes_enhancement.py
API route: POST /api/enhance/image
"""

from fastapi import APIRouter, UploadFile, File, Query
from fastapi.responses import Response

from app.core.enhancer import enhance_image, EnhancementConfig
from app.utils.image_utils import (
    validate_upload,
    read_image_bytes,
    bytes_to_pil,
    pil_to_bytes,
)

router = APIRouter()


@router.post(
    "/image",
    summary="Enhance image quality",
    response_description="Enhanced JPEG image",
)
async def enhance(
    file: UploadFile = File(...),
    denoise: bool = Query(True, description="Apply denoising"),
    denoise_h: float = Query(10.0, ge=1.0, le=30.0, description="Denoising strength (1-30)"),
    brightness: int = Query(0, ge=-100, le=100, description="Brightness offset (-100 to +100)"),
    contrast: float = Query(1.0, ge=0.5, le=3.0, description="Contrast multiplier (0.5-3.0)"),
    sharpen: bool = Query(False, description="Apply sharpening"),
    auto_wb: bool = Query(False, description="Auto white balance"),
):
    validate_upload(file)
    raw = await read_image_bytes(file)
    image = bytes_to_pil(raw)

    config = EnhancementConfig(
        denoise=denoise,
        denoise_h=denoise_h,
        brightness=brightness,
        contrast=contrast,
        sharpen=sharpen,
        auto_white_balance=auto_wb,
    )
    result = enhance_image(image, config)
    out_bytes = pil_to_bytes(result.convert("RGB"), fmt="JPEG")
    return Response(content=out_bytes, media_type="image/jpeg")