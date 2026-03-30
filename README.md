# 🤖 AI Image Intelligence Toolkit

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.9-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Tesseract](https://img.shields.io/badge/Tesseract-OCR-orange?style=for-the-badge)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Integrated-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

<br/>

**A modular AI system to process and enhance images using computer vision and machine learning.**  
Background removal · Image enhancement · Smart cropping · Multilingual OCR · Hugging Face AI

<br/>

[Features](#-features) · [Demo](#-demo) · [Installation](#-installation) · [API Docs](#-api-endpoints) · [Tech Stack](#-tech-stack) · [Contributing](#-contributing)

</div>

---

## ✨ Features

| Feature | Description | Technology |
|---|---|---|
| 🖼️ **Background Removal** | AI-based segmentation — outputs transparent PNG | `rembg` / `RMBG-1.4` (HF) |
| ✨ **Image Enhancement** | Denoise, brightness, contrast, sharpening | `OpenCV` / `Swin2SR` (HF) |
| ✂️ **Smart Cropping** | Face & object-aware auto cropping | `OpenCV Haar Cascade` |
| 🔤 **Multilingual OCR** | Extract text from images in 14 languages | `Tesseract` / `TrOCR` (HF) |
| 🔍 **Object Detection** | Detect & label objects with bounding boxes | `DETR ResNet-50` (HF) |

---

## 🖥️ Demo

```bash
# Start the server
uvicorn main:app --reload

# Open interactive UI
http://localhost:8000          ← Beautiful Web UI
http://localhost:8000/docs     ← Swagger API Docs
```

---

## 📁 Project Structure

```
ai-image-toolkit/
├── 📄 main.py                        ← FastAPI entry point
├── 📄 requirements.txt               ← Python dependencies
├── 📄 .env                           ← API keys (not committed)
├── 📄 index.html                     ← Frontend Web UI
│
├── 📂 app/
│   ├── 📂 api/                       ← API route handlers
│   │   ├── routes_background.py      ← POST /api/background/remove
│   │   ├── routes_enhancement.py     ← POST /api/enhance/image
│   │   ├── routes_crop.py            ← POST /api/crop/smart
│   │   ├── routes_ocr.py             ← POST /api/ocr/extract
│   │   └── routes_hf.py              ← POST /api/hf/* (Hugging Face)
│   │
│   ├── 📂 core/                      ← Business logic
│   │   ├── background_remover.py     ← rembg integration
│   │   ├── enhancer.py               ← OpenCV pipeline
│   │   ├── smart_cropper.py          ← Haar cascade + GrabCut
│   │   ├── ocr_engine.py             ← Tesseract multilingual
│   │   └── hf_client.py              ← Hugging Face API client
│   │
│   └── 📂 utils/
│       └── image_utils.py            ← Shared image helpers
│
├── 📂 tests/
│   └── test_all.py                   ← 18 unit tests
├── 📂 samples/                       ← Test images
└── 📂 docs/
    └── API.md                        ← Full API reference
```

---

## 🚀 Installation

### Prerequisites

- Python 3.10+
- Tesseract OCR

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-image-toolkit.git
cd ai-image-toolkit
```

### 2. Create virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Tesseract OCR

**Windows:**
```
Download from: https://github.com/UB-Mannheim/tesseract/wiki
Add to PATH: C:\Program Files\Tesseract-OCR
```

**Ubuntu/Debian:**
```bash
sudo apt install tesseract-ocr tesseract-ocr-hin tesseract-ocr-mar -y
```

**macOS:**
```bash
brew install tesseract tesseract-lang
```

### 5. Set up environment variables

Create a `.env` file in the project root:

```env
HF_API_KEY=hf_your_huggingface_token_here
```

Get your free API key at: **https://huggingface.co/settings/tokens**

### 6. Run the server

```bash
uvicorn main:app --reload
```

Visit **http://localhost:8000/docs** for the interactive API documentation.

---

## 📡 API Endpoints

### Core Features

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/background/remove` | Remove image background |
| `POST` | `/api/enhance/image` | Enhance image quality |
| `POST` | `/api/crop/smart` | Smart face/object crop |
| `POST` | `/api/ocr/extract` | Extract text (multilingual) |
| `GET` | `/api/ocr/languages` | List supported languages |

### Hugging Face AI

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/hf/status` | Check HF API connection |
| `POST` | `/api/hf/ocr` | TrOCR — accurate printed text |
| `POST` | `/api/hf/background-remove` | RMBG-1.4 — HD background removal |
| `POST` | `/api/hf/super-resolution` | Swin2SR — 2x image upscaling |
| `POST` | `/api/hf/object-detection` | DETR — object detection |

### Example Usage

```bash
# Background Removal
curl -X POST "http://localhost:8000/api/background/remove" \
     -F "file=@photo.jpg" --output result.png

# OCR — Hindi
curl -X POST "http://localhost:8000/api/ocr/extract?lang=hin" \
     -F "file=@document.jpg"

# Smart Crop — Face Mode
curl -X POST "http://localhost:8000/api/crop/smart?mode=face&width=400&height=400" \
     -F "file=@portrait.jpg" --output cropped.jpg

# HF Object Detection
curl -X POST "http://localhost:8000/api/hf/object-detection" \
     -F "file=@scene.jpg" --output detected.jpg
```

---

## 🌍 Supported OCR Languages

| Code | Language | Code | Language |
|---|---|---|---|
| `eng` | English | `hin` | Hindi |
| `mar` | Marathi | `ben` | Bengali |
| `guj` | Gujarati | `kan` | Kannada |
| `tam` | Tamil | `tel` | Telugu |
| `pan` | Punjabi | `ori` | Odia |
| `san` | Sanskrit | `eng+hin` | English + Hindi |
| `eng+mar` | English + Marathi | `eng+hin+mar` | All three |

---

## 🛠️ Tech Stack

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** — High performance Python API framework
- **[OpenCV](https://opencv.org/)** — Computer vision library
- **[Tesseract OCR](https://github.com/tesseract-ocr/tesseract)** — Multilingual text extraction
- **[rembg](https://github.com/danielgatis/rembg)** — U²-Net background removal
- **[Pillow](https://pillow.readthedocs.io/)** — Image processing
- **[NumPy](https://numpy.org/)** — Numerical computing

### AI / Machine Learning
- **[Hugging Face](https://huggingface.co/)** — AI model hub
  - `microsoft/trocr-large-printed` — OCR
  - `briaai/RMBG-1.4` — Background removal
  - `caidas/swin2SR-classical-sr-x2-64` — Super resolution
  - `facebook/detr-resnet-50` — Object detection

### Frontend
- Vanilla HTML/CSS/JS — Clean drag & drop UI

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

Expected output:
```
tests/test_all.py::TestEnhancer::test_returns_pil_image PASSED
tests/test_all.py::TestEnhancer::test_same_dimensions PASSED
...
18 passed in 12.3s
```

---

## 🔮 Future Enhancements

- [ ] YOLO v8 real-time object detection
- [ ] Batch image processing
- [ ] Docker deployment
- [ ] React frontend
- [ ] Image compression API
- [ ] Face recognition
- [ ] PDF text extraction

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m "Add amazing feature"`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

Made with ❤️ as part of an AI learning journey.

---

<div align="center">

⭐ **Star this repo if you found it helpful!** ⭐

</div>
