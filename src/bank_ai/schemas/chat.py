from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(slots=True)
class ChatRequest:
    question: str


@dataclass(slots=True)
class ChatResponse:
    answer: str
    route: str
    sources: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)
