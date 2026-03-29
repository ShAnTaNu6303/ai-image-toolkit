"""
AI Image Intelligence Toolkit
Entry point — mounts all feature routers and provides a health check.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_background import router as bg_router
from app.api.routes_enhancement import router as enhance_router
from app.api.routes_crop import router as crop_router
from app.api.routes_ocr import router as ocr_router

app = FastAPI(
    title="AI Image Intelligence Toolkit",
    description=(
        "Modular API for AI-powered image processing: "
        "background removal, enhancement, smart cropping, and multilingual OCR."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Feature routers
app.include_router(bg_router,      prefix="/api/background", tags=["Background Removal"])
app.include_router(enhance_router, prefix="/api/enhance",    tags=["Image Enhancement"])
app.include_router(crop_router,    prefix="/api/crop",       tags=["Smart Cropping"])
app.include_router(ocr_router,     prefix="/api/ocr",        tags=["OCR"])


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "AI Image Intelligence Toolkit"}


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to the AI Image Intelligence Toolkit",
        "docs": "/docs",
        "health": "/health",
    }