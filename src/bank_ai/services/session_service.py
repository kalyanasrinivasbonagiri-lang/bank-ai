from __future__ import annotations

from flask import session


class SessionService:
    def get_messages(self) -> list[dict]:
        return session.get("messages", [])

    def add_message(self, role: str, content: str) -> list[dict]:
        messages = self.get_messages()
        messages.append({"role": role, "content": content})
        session["messages"] = messages[-12:]
        session.modified = True
        return session["messages"]

    def clear(self) -> None:
        session["messages"] = []
        session["uploaded_context"] = ""
        session.modified = True

    def set_uploaded_context(self, text: str) -> None:
        session["uploaded_context"] = text
        session.modified = True

    def get_uploaded_context(self) -> str:
        return session.get("uploaded_context", "")
