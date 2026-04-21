from __future__ import annotations

from src.bank_ai.db.models import ChatRecord


class ChatRepository:
    def __init__(self):
        self._records: list[ChatRecord] = []

    def add(self, record: ChatRecord) -> None:
        self._records.append(record)

    def list_all(self) -> list[ChatRecord]:
        return list(self._records)
