from __future__ import annotations

from typing import Any

try:
    from groq import Groq
except ImportError:  # pragma: no cover
    Groq = None


def build_messages(system_prompt: str, user_prompt: str, context: str | None = None) -> list[dict[str, str]]:
    messages = [{"role": "system", "content": system_prompt.strip()}]
    if context:
        messages.append({"role": "user", "content": f"Context:\n{context.strip()}"})
    messages.append({"role": "user", "content": user_prompt.strip()})
    return messages


class GroqClient:
    def __init__(self, api_key: str, text_model: str, vision_model: str):
        self.api_key = api_key
        self.text_model = text_model
        self.vision_model = vision_model
        self._client = Groq(api_key=api_key) if api_key and Groq else None

    @property
    def enabled(self) -> bool:
        return self._client is not None

    def complete_text(self, messages: list[dict[str, Any]], temperature: float = 0.2) -> str:
        if not self._client:
            return self._fallback_text(messages)

        response = self._client.chat.completions.create(
            model=self.text_model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()

    def complete_vision(self, prompt: str, image_base64: str, mime_type: str = "image/png") -> str:
        if not self._client:
            return "OCR vision support is unavailable because GROQ_API_KEY is not configured."

        response = self._client.chat.completions.create(
            model=self.vision_model,
            messages=[
                {"role": "system", "content": "Extract and explain text from the uploaded banking document image."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{mime_type};base64,{image_base64}"},
                        },
                    ],
                },
            ],
            temperature=0.1,
        )
        return response.choices[0].message.content.strip()

    @staticmethod
    def _fallback_text(messages: list[dict[str, Any]]) -> str:
        user_messages = [message["content"] for message in messages if message["role"] == "user"]
        return (
            "BankAI is running without Groq configured. "
            "Please add GROQ_API_KEY for full answering support.\n\n"
            f"Latest request:\n{user_messages[-1] if user_messages else ''}"
        )
