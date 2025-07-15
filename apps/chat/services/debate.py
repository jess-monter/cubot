from apps.chat.engines.base import BaseChatEngine


class DebateService:
    def __init__(self, engine: BaseChatEngine):
        self.engine = engine

    def handle_turn(self, topic: str, messages: list) -> str:
        """
        Handles a turn in the debate by generating a reply based on the current topic and messages.
        """
        reply = self.engine.generate_reply(topic, messages)

        return reply
