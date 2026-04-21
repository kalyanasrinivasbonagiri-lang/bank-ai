from __future__ import annotations

from pathlib import Path


SUPPORTED_SOURCE_EXTENSIONS = {".txt", ".pdf"}


def iter_source_documents(root_dir: str | Path) -> list[Path]:
    root_path = Path(root_dir)
    if not root_path.exists():
        return []

    return sorted(
        path for path in root_path.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_SOURCE_EXTENSIONS
    )


def load_text_document(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")
