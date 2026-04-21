from __future__ import annotations

import base64
from pathlib import Path


def file_to_base64(path: str | Path) -> str:
    return encode_bytes_to_base64(Path(path).read_bytes())


def encode_bytes_to_base64(content: bytes) -> str:
    return base64.b64encode(content).decode("utf-8")


def ensure_text_file(path: str | Path, content: str) -> Path:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")
    return file_path
