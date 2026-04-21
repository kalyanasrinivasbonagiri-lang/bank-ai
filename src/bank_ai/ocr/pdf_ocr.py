from __future__ import annotations

from pathlib import Path

import fitz

from src.bank_ai.utils.file_utils import encode_bytes_to_base64


def extract_from_pdf(path: str | Path, groq_client, max_pages: int = 3) -> str:
    pdf_path = Path(path)
    if not pdf_path.exists():
        return ""

    document = fitz.open(pdf_path)
    collected_pages: list[str] = []
    try:
        for page_index in range(min(document.page_count, max_pages)):
            page = document.load_page(page_index)
            page_text = page.get_text("text").strip()
            if page_text:
                collected_pages.append(page_text)
                continue

            pixmap = page.get_pixmap()
            image_bytes = pixmap.tobytes("png")
            collected_pages.append(
                groq_client.complete_vision(
                    prompt="Read the banking PDF page and extract the visible text.",
                    image_base64=encode_bytes_to_base64(image_bytes),
                    mime_type="image/png",
                )
            )
    finally:
        document.close()

    return "\n\n".join(text for text in collected_pages if text)
