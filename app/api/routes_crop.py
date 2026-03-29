"""
app/api/routes_crop.py
API route: POST /api/crop/smart
"""

from fastapi import APIRouter, UploadFile, File, Query
from fastapi.responses import Response

from app.core.smart_cropper import smart_crop, CropMode
from app.utils.image_utils import (
    validate_upload,
    read_image_bytes,
    bytes_to_pil,
    pil_to_bytes,
)

router = APIRouter()


@router.post(
    "/smart",
    summary="Smart crop — face or object aware",
    response_description="Cropped and resized JPEG image",
)
async def smart_crop_endpoint(
    file: UploadFile = File(...),
    mode: CropMode = Query(
        "face",
        description="Detection mode: 'face', 'object', or 'center'",
    ),
    width: int = Query(512, ge=64, le=4096, description="Output width in pixels"),
    height: int = Query(512, ge=64, le=4096, description="Output height in pixels"),
    padding: float = Query(0.25, ge=0.0, le=1.0, description="Padding around detected region"),
):
    validate_upload(file)
    raw = await read_image_bytes(file)
    image = bytes_to_pil(raw)

    result = smart_crop(
        image,
        target_size=(width, height),
        mode=mode,
        padding_ratio=padding,
    )
    out_bytes = pil_to_bytes(result.convert("RGB"), fmt="JPEG")
    return Response(content=out_bytes, media_type="image/jpeg")