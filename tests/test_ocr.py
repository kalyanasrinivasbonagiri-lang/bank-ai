from __future__ import annotations

from pathlib import Path

from src.bank_ai.ocr.extraction import extract_text_from_file
from src.bank_ai.services.chat_service import ChatService


def test_text_file_extraction(app):
    with app.test_request_context("/"):
        sample_file = Path(app.config["UPLOAD_DIR"]) / "ocr_sample.txt"
        sample_file.write_text("Sample OCR text", encoding="utf-8")
        groq_client = ChatService(app.config).groq_client
        extracted = extract_text_from_file(sample_file, groq_client)
        assert extracted == "Sample OCR text"
