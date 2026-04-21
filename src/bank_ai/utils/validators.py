from __future__ import annotations

from pathlib import Path


def validate_question(question: str) -> str:
    cleaned = question.strip()
    if not cleaned:
        raise ValueError("Question is required.")
    return cleaned


def validate_upload_extension(filename: str, allowed_extensions: set[str]) -> None:
    suffix = Path(filename).suffix.lower()
    if suffix not in allowed_extensions:
        raise ValueError(f"Unsupported file type: {suffix}")
