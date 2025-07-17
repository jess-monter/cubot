import pytest
from apps.chat.models import Conversation, ConversationMessage
from apps.chat.services.conversation import ConversationService


@pytest.mark.django_db
def test_create_conversation():
    service = ConversationService()
    conversation = service.create_conversation("Flat Earth")

    assert Conversation.objects.count() == 1
    assert conversation.topic == "Flat Earth"


@pytest.mark.django_db
def test_add_message():
    service = ConversationService()
    conversation = Conversation.objects.create(topic="Flat Earth")

    service.add_message(conversation, "Hello", rol="user")

    messages = conversation.messages.all()
    assert messages.count() == 1
    assert messages[0].rol == "user"
    assert messages[0].message == "Hello"


@pytest.mark.django_db
def test_get_last_messages_returns_max_5():
    service = ConversationService()
    conversation = Conversation.objects.create(topic="Flat Earth")

    for i in range(10):
        ConversationMessage.objects.create(
            conversation=conversation, rol="user", message=f"Message {i+1}"
        )

    last_messages = service.get_last_messages(conversation)
    assert len(last_messages) == 5
    assert last_messages[0]["message"] == "Message 10"
    assert last_messages[-1]["message"] == "Message 6"


@pytest.mark.django_db
def test_get_last_messages_with_custom_limit():
    service = ConversationService()
    conversation = Conversation.objects.create(topic="Flat Earth")

    for i in range(7):
        ConversationMessage.objects.create(
            conversation=conversation, rol="bot", message=f"BotMsg {i+1}"
        )

    messages = service.get_last_messages(conversation, limit=3)
    assert len(messages) == 3
    assert messages[0]["message"] == "BotMsg 7"
    assert messages[-1]["message"] == "BotMsg 5"
