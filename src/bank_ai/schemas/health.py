from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(slots=True)
class HealthResponse:
    status: str
    app_name: str

    def to_dict(self) -> dict:
        return asdict(self)
