from __future__ import annotations

from src.bank_ai.constants.prompts import (
    FILE_SYSTEM_PROMPT,
    FOLLOW_UP_SYSTEM_PROMPT,
    GENERAL_SYSTEM_PROMPT,
    NO_CONTEXT_FALLBACK_PROMPT,
    SUMMARIZATION_SYSTEM_PROMPT,
)
from src.bank_ai.constants.settings import BANKING_DISCLAIMER
from src.bank_ai.llm.groq_client import GroqClient, build_messages
from src.bank_ai.llm.models import ChatAnswer
from src.bank_ai.rag.pipeline import RagPipeline
from src.bank_ai.services.response_service import ResponseService
from src.bank_ai.services.routing_service import RoutingService
from src.bank_ai.services.session_service import SessionService


class ChatService:
    def __init__(self, app_config):
        self.app_config = app_config
        self.groq_client = GroqClient(
            api_key=app_config["GROQ_API_KEY"],
            text_model=app_config["GROQ_TEXT_MODEL"],
            vision_model=app_config["GROQ_VISION_MODEL"],
        )
        self.routing_service = RoutingService(self.groq_client)
        self.response_service = ResponseService()
        self.session_service = SessionService()
        self.rag_pipeline = RagPipeline(app_config, self.groq_client)

    def answer(self, query: str) -> ChatAnswer:
        history = self.session_service.get_messages()
        uploaded_context = self.session_service.get_uploaded_context()
        route = self.routing_service.decide_route(
            query,
            has_upload_context=bool(uploaded_context),
            has_history=bool(history),
        )

        if route == "rag":
            rag_result = self.rag_pipeline.answer(query)
            answer = self.response_service.finalize_answer(rag_result["answer"], include_limitations=True)
            chat_answer = ChatAnswer(answer=answer, route=route, sources=rag_result["sources"])
        elif route == "upload":
            answer = self._answer_from_upload(query, uploaded_context)
            chat_answer = ChatAnswer(answer=answer, route=route, sources=[])
        elif route == "summarize":
            summary_target = uploaded_context or self._history_text(history)
            answer = self._simple_completion(SUMMARIZATION_SYSTEM_PROMPT, f"Summarize this:\n{summary_target}")
            chat_answer = ChatAnswer(answer=answer, route=route, sources=[])
        elif route == "follow_up":
            answer = self._simple_completion(
                FOLLOW_UP_SYSTEM_PROMPT,
                f"Conversation:\n{self._history_text(history)}\n\nFollow-up question:\n{query}",
            )
            chat_answer = ChatAnswer(answer=answer, route=route, sources=[])
        else:
            answer = self._simple_completion(
                GENERAL_SYSTEM_PROMPT,
                f"{query}\n\nRemember: {BANKING_DISCLAIMER}",
            )
            chat_answer = ChatAnswer(answer=answer, route=route, sources=[])

        self.session_service.add_message("user", query)
        self.session_service.add_message("assistant", chat_answer.answer)
        return chat_answer

    def _answer_from_upload(self, query: str, uploaded_context: str) -> str:
        if not uploaded_context.strip():
            return NO_CONTEXT_FALLBACK_PROMPT.strip()
        return self._simple_completion(FILE_SYSTEM_PROMPT, query, context=uploaded_context)

    def _simple_completion(self, system_prompt: str, user_prompt: str, context: str | None = None) -> str:
        messages = build_messages(system_prompt, user_prompt, context=context)
        return self.groq_client.complete_text(messages)

    @staticmethod
    def _history_text(history: list[dict]) -> str:
        if not history:
            return ""
        return "\n".join(f"{item['role']}: {item['content']}" for item in history[-8:])
