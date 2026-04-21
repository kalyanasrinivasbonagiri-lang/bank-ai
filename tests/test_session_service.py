from __future__ import annotations

from src.bank_ai.services.session_service import SessionService


def test_session_message_flow(app):
    service = SessionService()
    with app.test_request_context("/"):
        service.add_message("user", "How to deposit money?")
        service.add_message("assistant", "Use the deposit slip and submit it.")
        messages = service.get_messages()
        assert len(messages) == 2
        assert messages[0]["role"] == "user"
