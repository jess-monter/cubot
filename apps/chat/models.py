from django.db import models

import uuid


class Conversation(models.Model):
    """Model representing a conversation."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Conversation {self.id}"


class ConversationMessage(models.Model):
    """Model representing a message in a conversation."""

    ROL_CHOICES = [
        ("user", "user"),
        ("bot", "bot"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default="user")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Message {self.id} in Conversation {self.conversation.id}"
