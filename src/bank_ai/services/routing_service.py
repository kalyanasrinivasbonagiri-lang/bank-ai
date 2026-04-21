from __future__ import annotations

from src.bank_ai.constants.prompts import ROUTER_SYSTEM_PROMPT
from src.bank_ai.constants.routing import ROUTE_KEYWORDS
from src.bank_ai.llm.groq_client import build_messages


class RoutingService:
    def __init__(self, groq_client):
        self.groq_client = groq_client

    def decide_route(self, query: str, has_upload_context: bool = False, has_history: bool = False) -> str:
        lowered = query.lower().strip()

        if has_upload_context and any(word in lowered for word in ("this file", "uploaded", "document", "form")):
            return "upload"
        if any(word in lowered for word in ROUTE_KEYWORDS["summarize"]):
            return "summarize"
        if has_history and len(lowered.split()) <= 7:
            return "follow_up"
        if any(word in lowered for word in ROUTE_KEYWORDS["rag"]):
            return "rag"
        if any(word in lowered for word in ROUTE_KEYWORDS["upload"]):
            return "upload"

        route = self.groq_client.complete_text(build_messages(ROUTER_SYSTEM_PROMPT, query), temperature=0.0).lower()
        return route if route in {"general", "rag", "upload", "summarize", "follow_up"} else "general"
