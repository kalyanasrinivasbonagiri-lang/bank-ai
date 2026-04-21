from __future__ import annotations

from markupsafe import escape


def sanitize_user_text(text: str) -> str:
    return str(escape(text.strip()))
