from pathlib import Path
from pypdf import PdfReader
from ocr import load_scanned_pdf

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "raw"


def load_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        extracted_text = page.extract_text()

        if extracted_text:
            text += extracted_text + "\n"

    return text.strip()


def load_txt(txt_file):
    with open(txt_file, "r", encoding="utf-8", errors="ignore") as file:
        return file.read().strip()


def load_documents():
    documents = []

    for file in DATA_DIR.rglob("*"):

        if not file.is_file():
            continue

        if file.suffix.lower() == ".pdf":
            text = load_pdf(file)

            if not text.strip():
                print(f"Ocr Fallback:{file.name}")
                text=load_scanned_pdf(file)

        elif file.suffix.lower() == ".txt":
            text = load_txt(file)

        else:
            continue

        if not text:
            print(f"Warning: No text extracted from {file.name}")
            continue

        doc = {
            "filename": file.name,
            "source": file.parent.name,
            "path": str(file.relative_to(DATA_DIR)),
            "extension": file.suffix.lower(),
            "text": text,
        }

        documents.append(doc)

    return documents


if __name__ == "__main__":
    docs = load_documents()

    print(f"\nLoaded {len(docs)} documents\n")

    for doc in docs:
        print("=" * 60)
        print(f"Filename  : {doc['filename']}")
        print(f"Source    : {doc['source']}")
        print(f"Extension : {doc['extension']}")
        print(f"Path      : {doc['path']}")
        print(f"Characters: {len(doc['text'])}")