from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(slots=True)
class UploadResponse:
    filename: str
    extracted_text: str

    def to_dict(self) -> dict:
        return asdict(self)
