"""
app/api/routes_background.py
API route: POST /api/background/remove
"""

from fastapi import APIRouter, UploadFile, File, Query
from fastapi.responses import Response, JSONResponse

from app.core.background_remover import remove_background, add_solid_background
from app.utils.image_utils import (
    validate_upload,
    read_image_bytes,
    bytes_to_pil,
    pil_to_bytes,
    image_size_info,
)

router = APIRouter()


@router.post(
    "/remove",
    summary="Remove image background",
    response_description="PNG image with transparent background",
)
async def remove_bg(
    file: UploadFile = File(..., description="Input image (JPEG, PNG, WEBP)"),
    bg_color: str = Query(
        default="transparent",
        description="'transparent' returns RGBA PNG. Hex value e.g. 'ffffff' fills with colour.",
    ),
):
    validate_upload(file)
    raw = await read_image_bytes(file)
    image = bytes_to_pil(raw)

    result = remove_background(image)

    if bg_color.lower() == "transparent":
        out_bytes = pil_to_bytes(result, fmt="PNG")
        return Response(content=out_bytes, media_type="image/png")
    else:
        try:
            hex_clean = bg_color.lstrip("#")
            r, g, b = int(hex_clean[0:2], 16), int(hex_clean[2:4], 16), int(hex_clean[4:6], 16)
        except (ValueError, IndexError):
            return JSONResponse(
                status_code=422,
                content={"detail": "Invalid bg_color. Use 'transparent' or a 6-digit hex like 'ffffff'."},
            )
        filled = add_solid_background(result, color=(r, g, b))
        out_bytes = pil_to_bytes(filled, fmt="JPEG")
        return Response(content=out_bytes, media_type="image/jpeg")