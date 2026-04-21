from __future__ import annotations

from src.bank_ai.services.chat_service import ChatService


def test_general_route_answer_includes_bankai_scope(app):
    with app.test_request_context("/"):
        service = ChatService(app.config)
        result = service.answer("Hello")
        assert result.route in {"general", "follow_up"}
        assert "BankAI" in result.answer
