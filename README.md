# 🤖 AI Image Intelligence Toolkit

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.9-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Tesseract](https://img.shields.io/badge/Tesseract-OCR-orange?style=for-the-badge)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Integrated-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A modular AI system to process and enhance images using computer vision and machine learning.**
Background removal · Image enhancement · Smart cropping · Multilingual OCR · Hugging Face AI

[Features](#-features) · [Demo](#-demo) · [Installation](#-installation) · [API Docs](#-api-endpoints) · [Tech Stack](#-tech-stack)

</div>

---

## 🎬 Demo

### 🖼️ Background Removal
> AI automatically detects the subject and removes the background — outputs a clean transparent PNG.

| Before | After |
|:---:|:---:|
| ![Before](samples/bg_before.jpg) | ![After](samples/bg_after.png) |

---

### ✨ Image Enhancement
> Automatically denoises, adjusts brightness/contrast and sharpens the image.

| Before | After |
|:---:|:---:|
| ![Before](samples/enhance_before.jpg) | ![After](samples/enhance_after.jpg) |

---

### 🔤 OCR — Multilingual Text Extraction
> Extracts text from images. Tested on a real Hackathon poster — 68 words detected!

| Input Image | Extracted Output |
|:---:|:---:|
| ![OCR Input](samples/ocr_input.png) | ![OCR Result](samples/ocr_result.png) |

```
BHARATI VIDYAPEETH (DEEMED TO BE UNIVERSITY)
COLLEGE OF ENGINEERING, PUNE
TECH SPRINT HACKATHON
Last Date to Register: 10th January 2026
Team size 1-4 | Mode - Hybrid
Words: 68 | Confidence: 47.4%
```

---

## ✨ Features

| Feature | Description | Technology |
|---|---|---|
| 🖼️ **Background Removal** | AI segmentation — transparent PNG output | `rembg` / `RMBG-1.4` (HF) |
| ✨ **Image Enhancement** | Denoise, brightness, contrast, sharpening | `OpenCV` / `Swin2SR` (HF) |
| ✂️ **Smart Cropping** | Face & object-aware auto cropping | `OpenCV Haar Cascade` |
| 🔤 **Multilingual OCR** | Extract text in 14 Indian languages | `Tesseract` / `TrOCR` (HF) |
| 🔍 **Object Detection** | Detect & label objects with bounding boxes | `DETR ResNet-50` (HF) |

---

## 🖥️ Web UI

A clean, modern drag-and-drop web interface — no Swagger needed!

```bash
uvicorn main:app --reload
# Open: http://localhost:8000
```

---

## 📁 Project Structure

```
ai-image-toolkit/
├── main.py                    ← FastAPI entry point
├── requirements.txt           ← Python dependencies
├── index.html                 ← Frontend Web UI
├── .env                       ← API keys (not committed)
├── app/
│   ├── api/
│   │   ├── routes_background.py
│   │   ├── routes_enhancement.py
│   │   ├── routes_crop.py
│   │   ├── routes_ocr.py
│   │   └── routes_hf.py       ← Hugging Face routes
│   ├── core/
│   │   ├── background_remover.py
│   │   ├── enhancer.py
│   │   ├── smart_cropper.py
│   │   ├── ocr_engine.py
│   │   └── hf_client.py       ← HF API client
│   └── utils/
│       └── image_utils.py
├── tests/
│   └── test_all.py            ← 18 unit tests
└── samples/                   ← Demo images
```

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/ShAnTaNu6303/ai-image-toolkit.git
cd ai-image-toolkit
```

### 2. Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Tesseract OCR

**Windows:** Download from https://github.com/UB-Mannheim/tesseract/wiki
```
Add to PATH: C:\Program Files\Tesseract-OCR
```

**Ubuntu:**
```bash
sudo apt install tesseract-ocr tesseract-ocr-hin tesseract-ocr-mar -y
```

### 5. Add API Key
Create `.env` file:
```
HF_API_KEY=hf_your_token_here
```
Get free token: https://huggingface.co/settings/tokens

### 6. Run
```bash
uvicorn main:app --reload
```

---

## 📡 API Endpoints

### Core
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/background/remove` | Remove background |
| `POST` | `/api/enhance/image` | Enhance quality |
| `POST` | `/api/crop/smart` | Smart crop |
| `POST` | `/api/ocr/extract` | Extract text |
| `GET` | `/api/ocr/languages` | Supported languages |

### Hugging Face AI
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/hf/status` | Connection check |
| `POST` | `/api/hf/ocr` | TrOCR accurate OCR |
| `POST` | `/api/hf/background-remove` | RMBG-1.4 HD removal |
| `POST` | `/api/hf/super-resolution` | Swin2SR 2x upscale |
| `POST` | `/api/hf/object-detection` | DETR detection |

---

## 🌍 Supported OCR Languages

| Code | Language | Code | Language |
|---|---|---|---|
| `eng` | English | `hin` | Hindi |
| `mar` | Marathi | `ben` | Bengali |
| `guj` | Gujarati | `kan` | Kannada |
| `tam` | Tamil | `tel` | Telugu |
| `pan` | Punjabi | `ori` | Odia |
| `eng+hin` | English + Hindi | `eng+hin+mar` | All three |

---

## 🛠️ Tech Stack

- **FastAPI** — REST API framework
- **OpenCV** — Computer vision
- **Tesseract OCR** — Multilingual text extraction
- **rembg** — U²-Net background removal
- **Pillow + NumPy** — Image processing
- **Hugging Face** — AI models (TrOCR, RMBG, Swin2SR, DETR)

---

## 🧪 Tests

```bash
pytest tests/ -v
# 18 passed
```

---

## 🔮 Future Enhancements

- [ ] YOLO v8 object detection
- [ ] Batch processing
- [ ] Docker deployment
- [ ] React frontend
- [ ] PDF text extraction

---

## 👨‍💻 Author

Made with ❤️ by **ShAnTaNu6303**

<div align="center">

⭐ **Star this repo if you found it helpful!** ⭐

</div>