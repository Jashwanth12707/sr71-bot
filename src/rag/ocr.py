from pathlib import Path
import io
import os

import pymupdf
import pytesseract
from PIL import Image
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(str(BASE_DIR / ".env"), override=True)

tesseract_path = os.getenv("TESSERACT_PATH")
tessdata_path = os.getenv("TESSDATA_PREFIX")

if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

if tessdata_path:
    os.environ["TESSDATA_PREFIX"] = tessdata_path


def load_scanned_pdf(pdf_file):
    txt_file = pdf_file.with_suffix(".txt")

    if txt_file.exists():
        print(f"Using cached OCR: {txt_file.name}")

        with open(txt_file, "r", encoding="utf-8") as f:
            return f.read()

    document = pymupdf.open(pdf_file)

    pages = []

    total_pages = len(document)

    for i, page in enumerate(document, start=1):
        print(f"OCR: {pdf_file.name} | Page {i}/{total_pages}")

        pix = page.get_pixmap(dpi=200)

        image = Image.open(
            io.BytesIO(
                pix.tobytes("png")
            )
        )

        extracted_text = pytesseract.image_to_string(
            image,
            lang="eng"
        )

        if extracted_text:
            pages.append(extracted_text)

    document.close()

    text = "\n".join(pages).strip()

    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Saved OCR cache: {txt_file.name}")

    return text