from __future__ import annotations

from src.bank_ai.constants.prompts import NO_CONTEXT_FALLBACK_PROMPT, RAG_SYSTEM_PROMPT
from src.bank_ai.llm.groq_client import build_messages
from src.bank_ai.rag.retrieval import retrieve_context
from src.bank_ai.services.response_service import (
    build_answer_style_instruction,
    build_source_list,
    format_context_block,
)


class RagPipeline:
    def __init__(self, app_config, groq_client):
        self.app_config = app_config
        self.groq_client = groq_client

    def answer(self, query: str) -> dict:
        documents = retrieve_context(query, self.app_config)
        if not documents:
            return {
                "answer": NO_CONTEXT_FALLBACK_PROMPT.strip(),
                "sources": [],
            }

        context = format_context_block(documents)
        styled_query = f"{query}\n\n{build_answer_style_instruction(query)}"
        messages = build_messages(RAG_SYSTEM_PROMPT, styled_query, context=context)
        answer = self.groq_client.complete_text(messages)
        return {
            "answer": answer,
            "sources": build_source_list(documents),
        }
