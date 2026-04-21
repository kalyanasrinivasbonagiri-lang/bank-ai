from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RetrievalResult:
    answer: str
    sources: list[dict]
