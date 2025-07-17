import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.chat.models import Conversation, ConversationMessage
from unittest.mock import patch, MagicMock

pytestmark = pytest.mark.django_db

client = APIClient()


def test_create_new_conversation():
    url = reverse("conversation-list")
    response = client.post(url, {"message": "Flat Earth"}, format="json")

    assert response.status_code == 200
    assert Conversation.objects.count() == 1
    conversation = Conversation.objects.first()
    assert conversation.topic == "Flat Earth"


@patch("apps.chat.views.OllamaChatEngine")
def test_reply_to_existing_conversation(mock_engine_cls):
    url = reverse("conversation-list")

    # Setup mock engine
    mock_engine = MagicMock()
    mock_engine.generate_reply.return_value = "Bot reply"
    mock_engine_cls.return_value = mock_engine

    # Create a conversation and a message
    conversation = Conversation.objects.create(topic="Flat Earth")
    ConversationMessage.objects.create(conversation=conversation, rol="user", message="Hello")

    response = client.post(
        url,
        {"conversation_id": str(conversation.id), "message": "How do you explain gravity?"},
        format="json",
    )

    assert response.status_code == 200
    conversation.refresh_from_db()
    messages = conversation.messages.all()
    assert messages.count() == 3  # user + user + bot
    assert messages.last().rol == "user"


def test_conversation_not_found():
    url = reverse("conversation-list")
    response = client.post(
        url,
        {"conversation_id": "00000000-0000-0000-0000-000000000000", "message": "Hello"},
        format="json",
    )
    assert response.status_code == 404
    assert response.data["error"] == "Conversation not found"
