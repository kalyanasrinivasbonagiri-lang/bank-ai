from __future__ import annotations

from src.bank_ai.services.response_service import build_answer_style_instruction


def test_broad_process_question_prefers_customer_service_summary():
    instruction = build_answer_style_instruction("How to open a bank account?")

    assert "helpful bank counter assistant" in instruction
    assert "Do not jump straight into a long numbered list" in instruction
    assert "Offer to provide step-by-step instructions" in instruction


def test_explicit_step_question_prefers_numbered_steps():
    instruction = build_answer_style_instruction("Can you give me steps to open a bank account?")

    assert "numbered steps" in instruction
    assert "This is the process" in instruction
    assert "5 to 8 steps" in instruction
