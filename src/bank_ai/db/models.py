from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ChatRecord:
    role: str
    content: str
