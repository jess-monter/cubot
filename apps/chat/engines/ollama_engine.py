from typing import List, Dict

import httpx

from django.conf import settings

from apps.chat.engines.base import BaseChatEngine
from apps.chat.prompts import SYSTEM_PROMPT, get_intro_message
from apps.llm_experiments.services import get_active_model_prompt


class OllamaChatEngine(BaseChatEngine):

    def __init__(self):
        active_modelprompt = get_active_model_prompt()
        self.model = active_modelprompt.llm_model if active_modelprompt else settings.OLLAMA_MODEL
        self.prompt = active_modelprompt.prompt if active_modelprompt else SYSTEM_PROMPT
        self.host = settings.OLLAMA_HOST

    def generate_reply(self, topic: str, messages: list) -> str:
        prompt = self.format_prompt(messages, topic)

        response = httpx.post(
            f"{self.host}/api/chat",
            json={
                "model": self.model,
                "messages": prompt,
                "temperature": 0.9,
                "stream": False,
            },
            timeout=60.0,
        )
        response.raise_for_status()
        return response.json()["response"].strip()

    def format_prompt(self, messages: list, topic: str) -> List[Dict]:
        system_message = self.prompt.strip() + "\n\n" + get_intro_message(topic).strip()
        prompt = [{"role": "system", "content": system_message}]
        for msg in messages:
            role = msg["rol"]
            content = msg["message"].strip()
            if role == "user":
                prompt.append({"role": "user", "content": content})
            elif role == "bot":
                prompt.append({"role": "assistant", "content": content})
        return prompt
