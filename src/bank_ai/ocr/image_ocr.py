from __future__ import annotations

from pathlib import Path

from src.bank_ai.utils.file_utils import file_to_base64


def extract_from_image(path: str | Path, groq_client) -> str:
    image_path = Path(path)
    if not image_path.exists():
        return ""

    image_base64 = file_to_base64(image_path)
    suffix = image_path.suffix.lower()
    mime_type = "image/png" if suffix == ".png" else "image/jpeg"
    return groq_client.complete_vision(
        prompt="Read the banking document image. Extract visible text and explain important fields if obvious.",
        image_base64=image_base64,
        mime_type=mime_type,
    )
