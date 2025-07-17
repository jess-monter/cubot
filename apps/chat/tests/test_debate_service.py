from apps.chat.services.debate import DebateService
from apps.chat.engines.base import BaseChatEngine


class FakeChatEngine(BaseChatEngine):
    def generate_reply(self, topic: str, messages: list) -> str:
        return f"Fake reply to topic '{topic}' with {len(messages)} messages."


def test_handle_turn_generates_reply():
    fake_engine = FakeChatEngine()
    service = DebateService(engine=fake_engine)

    topic = "Is AI good for society?"
    messages = [
        {"rol": "user", "message": "Yes, AI is transforming healthcare and education."},
        {"rol": "bot", "message": "But what about job displacement?"},
    ]

    response = service.handle_turn(topic, messages)

    assert response == "Fake reply to topic 'Is AI good for society?' with 2 messages."
