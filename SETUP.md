# 📝 AI-Powered Document Reader Setup & Progress Guide  
> Documenting installation, development, and testing steps (as of March 27, 2025)

---

## ✅ Project Overview

This project is a web-based tool that helps low-vision users access documents containing both text and images. It uses:

- **Tesseract OCR** for text extraction
- **Hugging Face transformer models** (e.g., BLIP) for image captioning
- **Gradio or Streamlit** for an accessible web interface

---

## 🗂 Project Folder Structure
```
Neural-network-project/
├── core/
│   ├── ocr.py
│   └── __init__.py
├── ocr_test_module.py
├── sample.jpg / sample.pdf
├── README.md / SETUP.md
```

---

## 🔧 Step-by-Step Setup

### 1. 🟢 GitHub Setup
- Created a GitHub repository: `AI-Powered-Document-Reader-for-BLV-Users`
- Initialized repo with folders and files:
  - `core/ocr.py`: OCR logic module
  - `ocr_test_module.py`: Test script
  - `README.md`: Project overview

---

### 2. 💻 Development Environment (macOS)

#### Installed system dependencies via **Homebrew**:
```bash
brew install tesseract
brew install poppler
```

These install:
- `tesseract`: for OCR
- `pdfinfo`, `pdftoppm`: for PDF-to-image conversion

---

### 3. 🐍 Python Virtual Environment *(optional)*
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 4. 📦 Installed Required Python Packages
Used `pip` to install:

```bash
pip install pytesseract pdf2image Pillow
```

Also added:
- `transformers`, `torch` (for BLIP — to be added later)
- `gradio` or `streamlit` (for web UI — to be added later)

---

### 5. ✅ Created and Tested OCR Module

#### `core/ocr.py`:
- Contains two functions:
```python
def extract_text_from_image(image_path):
    # Uses pytesseract on an image
    ...

def extract_text_from_pdf(pdf_path):
    # Converts PDF pages to images, runs OCR on each
    ...
```

#### Note:
- Used `poppler_path="/opt/homebrew/bin"` in `convert_from_path()` to avoid PDFInfo errors on macOS/Anaconda.

---

### 6. 🧪 Tested with `ocr_test_module.py`
```python
from core.ocr import extract_text_from_image, extract_text_from_pdf

print(extract_text_from_image("sample.jpg"))
print(extract_text_from_pdf("sample.pdf"))
```

Ran the test successfully:
```bash
python ocr_test_module.py
```

Fixed common issues:
- 🛠 ModuleNotFoundError: added `__init__.py` and updated `sys.path`
- 🛠 PDFPageCountError: confirmed correct Poppler installation
- 🛠 Wrong input: used real PDFs, not renamed `.jpg` files

---

## ✅ Current Status

- OCR and text to speech work for both images and PDFs
- Output is stored in the folder "outputs" as an mp3 extension
- Project modules are structured and reusable
- Next step: integrate **BLIP for image captioning** and build **web app UI**

---

## 🔜 Next Steps
- [ ] Add `core/captioning.py` to generate captions using BLIP
- [ ] Build web UI using Gradio/Streamlit
- [ ] Add text-to-speech and accessibility features
- [ ] Start user feedback/testing phase
