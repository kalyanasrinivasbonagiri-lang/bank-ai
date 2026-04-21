from __future__ import annotations

from pathlib import Path

from src.bank_ai.ocr.image_ocr import extract_from_image
from src.bank_ai.ocr.pdf_ocr import extract_from_pdf


def extract_text_from_file(path: str | Path, groq_client) -> str:
    file_path = Path(path)
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return extract_from_pdf(file_path, groq_client)
    if suffix in {".png", ".jpg", ".jpeg"}:
        return extract_from_image(file_path, groq_client)
    if suffix == ".txt":
        return file_path.read_text(encoding="utf-8")
    return ""
