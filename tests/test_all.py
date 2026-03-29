"""
tests/test_all.py
Unit tests for all four toolkit modules.
Run with: pytest tests/ -v
"""

import io
import numpy as np
import pytest
from PIL import Image, ImageDraw


# ── Fixtures ──────────────────────────────────────────────────────────────────

def _make_rgb_image(w: int = 256, h: int = 256, color=(120, 180, 60)) -> Image.Image:
    return Image.new("RGB", (w, h), color=color)


def _make_noisy_image(w: int = 256, h: int = 256) -> Image.Image:
    rng = np.random.default_rng(42)
    arr = rng.integers(0, 256, (h, w, 3), dtype=np.uint8)
    return Image.fromarray(arr, mode="RGB")


def _make_text_image(text: str = "Hello World", w: int = 400, h: int = 100) -> Image.Image:
    img = Image.new("RGB", (w, h), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((20, 30), text, fill=(0, 0, 0))
    return img


# ── Enhancement tests ─────────────────────────────────────────────────────────

class TestEnhancer:
    def test_returns_pil_image(self):
        from app.core.enhancer import enhance_image
        img = _make_rgb_image()
        result = enhance_image(img)
        assert isinstance(result, Image.Image)

    def test_same_dimensions(self):
        from app.core.enhancer import enhance_image, EnhancementConfig
        img = _make_rgb_image(320, 240)
        result = enhance_image(img, EnhancementConfig(denoise=True, brightness=20, contrast=1.2))
        assert result.size == (320, 240)

    def test_brightness_increases_mean(self):
        from app.core.enhancer import enhance_image, EnhancementConfig
        img = Image.new("RGB", (64, 64), color=(100, 100, 100))
        result = enhance_image(img, EnhancementConfig(denoise=False, brightness=50))
        mean_before = np.array(img).mean()
        mean_after = np.array(result).mean()
        assert mean_after > mean_before

    def test_sharpen_option(self):
        from app.core.enhancer import enhance_image, EnhancementConfig
        img = _make_noisy_image()
        result = enhance_image(img, EnhancementConfig(denoise=False, sharpen=True))
        assert result.size == img.size

    def test_auto_white_balance(self):
        from app.core.enhancer import enhance_image, EnhancementConfig
        img = Image.new("RGB", (64, 64), color=(200, 100, 50))
        result = enhance_image(img, EnhancementConfig(denoise=False, auto_white_balance=True))
        assert isinstance(result, Image.Image)


# ── Smart Cropper tests ───────────────────────────────────────────────────────

class TestSmartCropper:
    def test_center_crop_output_size(self):
        from app.core.smart_cropper import smart_crop
        img = _make_rgb_image(640, 480)
        result = smart_crop(img, target_size=(224, 224), mode="center")
        assert result.size == (224, 224)

    def test_face_mode_no_face_falls_back(self):
        from app.core.smart_cropper import smart_crop
        img = _make_rgb_image(300, 300)
        result = smart_crop(img, target_size=(128, 128), mode="face")
        assert result.size == (128, 128)

    def test_object_mode_returns_correct_size(self):
        from app.core.smart_cropper import smart_crop
        img = _make_rgb_image(300, 300)
        result = smart_crop(img, target_size=(200, 200), mode="object")
        assert result.size == (200, 200)

    def test_returns_pil_image(self):
        from app.core.smart_cropper import smart_crop
        img = _make_rgb_image()
        assert isinstance(smart_crop(img, mode="center"), Image.Image)


# ── OCR Engine tests ──────────────────────────────────────────────────────────

class TestOCREngine:
    def test_returns_ocr_result(self):
        from app.core.ocr_engine import extract_text, OCRResult
        img = _make_text_image("Test OCR")
        result = extract_text(img, lang="eng")
        assert isinstance(result, OCRResult)

    def test_word_count_positive(self):
        from app.core.ocr_engine import extract_text
        img = _make_text_image("Hello World")
        result = extract_text(img, lang="eng")
        assert isinstance(result.word_count, int)
        assert result.word_count >= 0

    def test_lines_is_list(self):
        from app.core.ocr_engine import extract_text
        img = _make_text_image("Line one")
        result = extract_text(img, lang="eng")
        assert isinstance(result.lines, list)

    def test_unsupported_language_raises(self):
        from app.core.ocr_engine import extract_text
        img = _make_text_image()
        with pytest.raises(ValueError, match="Unsupported language"):
            extract_text(img, lang="xyz")

    def test_preprocess_false_still_works(self):
        from app.core.ocr_engine import extract_text
        img = _make_text_image("No preprocess")
        result = extract_text(img, lang="eng", preprocess=False)
        assert isinstance(result.text, str)


# ── Image Utils tests ─────────────────────────────────────────────────────────

class TestImageUtils:
    def test_pil_cv2_roundtrip(self):
        from app.utils.image_utils import pil_to_cv2, cv2_to_pil
        img = _make_rgb_image(100, 100, color=(10, 200, 100))
        arr = pil_to_cv2(img)
        restored = cv2_to_pil(arr)
        assert restored.size == img.size
        assert restored.mode == "RGB"

    def test_pil_to_bytes_png(self):
        from app.utils.image_utils import pil_to_bytes
        img = _make_rgb_image()
        data = pil_to_bytes(img, fmt="PNG")
        assert data[:4] == b"\x89PNG"

    def test_bytes_to_pil(self):
        from app.utils.image_utils import bytes_to_pil, pil_to_bytes
        img = _make_rgb_image(50, 50)
        data = pil_to_bytes(img, fmt="PNG")
        restored = bytes_to_pil(data)
        assert restored.size == (50, 50)

    def test_image_size_info(self):
        from app.utils.image_utils import image_size_info
        img = _make_rgb_image(123, 456)
        info = image_size_info(img)
        assert info["width"] == 123
        assert info["height"] == 456