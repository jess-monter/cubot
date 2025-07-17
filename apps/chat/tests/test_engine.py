import pytest
from apps.chat.engines.ollama_engine import OllamaChatEngine


@pytest.fixture
def engine():
    return OllamaChatEngine()


@pytest.mark.django_db
def test_format_prompt_output_structure(engine):
    messages = [
        {"rol": "user", "message": "Is the Earth really flat?"},
        {"rol": "bot", "message": "Have you ever seen the curve yourself?"},
        {"rol": "user", "message": "Yes, from a plane."},
        {"rol": "bot", "message": "Airplane windows are curved. That could be deceptive."},
        {"rol": "user", "message": "Still, I trust science."},
    ]
    topic = "Convince me that the earth is flat"

    prompt = engine.format_prompt(messages, topic)

    assert prompt.startswith("The topic is"), "Prompt must start with topic intro"
    assert "User: Still, I trust science." in prompt
    assert prompt.strip().endswith("Bot:"), "Prompt must end with 'Bot:'"


@pytest.mark.django_db
def test_prompt_maintains_message_order(engine):
    messages = [
        {"rol": "user", "message": "Q1"},
        {"rol": "bot", "message": "A1"},
        {"rol": "user", "message": "Q2"},
    ]
    topic = "Convince me that the earth is flat"
    prompt = engine.format_prompt(messages, topic)

    assert prompt.index("User: Q1") < prompt.index("Bot: A1") < prompt.index("User: Q2")


@pytest.mark.django_db
def test_prompt_supports_fewer_than_5_messages(engine):
    messages = [
        {"rol": "user", "message": "Why would NASA lie?"},
        {
            "rol": "bot",
            "message": "There are political motives, funding incentives, and control of narratives.",
        },
    ]
    topic = "Convince me that the earth is flat"
    prompt = engine.format_prompt(messages, topic)

    assert "Why would NASA lie?" in prompt
    assert prompt.count("User:") == 1
    assert prompt.count("Bot:") == 2  # last line is 'Bot:' to continue
