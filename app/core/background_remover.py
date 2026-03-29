"""
app/core/background_remover.py
Removes image backgrounds using the rembg library (U2-Net model).
"""

import io
from PIL import Image


def remove_background(image: Image.Image) -> Image.Image:
    try:
        from rembg import remove
    except ImportError as exc:
        raise RuntimeError(
            "rembg is not installed. Run: pip install rembg"
        ) from exc

    buf_in = io.BytesIO()
    image.convert("RGB").save(buf_in, format="PNG")
    result_bytes = remove(buf_in.getvalue())
    return Image.open(io.BytesIO(result_bytes)).convert("RGBA")


def add_solid_background(
    image: Image.Image,
    color: tuple = (255, 255, 255),
) -> Image.Image:
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    background = Image.new("RGBA", image.size, (*color, 255))
    composite = Image.alpha_composite(background, image)
    return composite.convert("RGB")