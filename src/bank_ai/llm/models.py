from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ChatAnswer:
    answer: str
    route: str
    sources: list[dict] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass(slots=True)
class RouteDecision:
    route: str
    reason: str = ""
