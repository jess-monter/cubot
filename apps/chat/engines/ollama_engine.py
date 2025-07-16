import httpx

from django.conf import settings

from apps.chat.engines.base import BaseChatEngine
from apps.chat.prompts import SYSTEM_PROMPT, get_intro_message


class OllamaChatEngine(BaseChatEngine):

    def __init__(self, model: str = "phi3"):
        self.model = model
        self.host = settings.OLLAMA_HOST or "http://localhost:11434"

    def generate_reply(self, topic: str, messages: list) -> str:
        prompt = self.format_prompt(messages, topic)

        response = httpx.post(
            f"{self.host}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "system": SYSTEM_PROMPT,
                "temperature": 0.9,
                "stop": ["User:", "Bot:"],
                "stream": False,
            },
            timeout=60.0,
        )
        response.raise_for_status()
        return response.json()["response"].strip()

    def format_prompt(self, messages: list, topic: str) -> str:
        lines = [get_intro_message(topic).strip(), ""]
        for msg in messages:
            role = msg["rol"]
            if role == "user":
                lines.append(f"User: {msg['message'].strip()}")
            elif role == "bot":
                lines.append(f"Bot: {msg['message'].strip()}")

        lines.append("Bot:")  # ← model continues here
        return "\n".join(lines)
