from typing import List, Dict
from apps.chat.models import Conversation, ConversationMessage


class ConversationService:
    def create_conversation(self, message_text: str) -> Conversation:
        return Conversation.objects.create(topic=message_text)

    def add_message(self, conversation: Conversation, message_text: str, rol: str) -> None:
        ConversationMessage.objects.create(conversation=conversation, rol=rol, message=message_text)

    def get_last_messages(self, conversation: Conversation, limit: int = 5) -> List[Dict]:
        return [{"rol": m.rol, "message": m.message} for m in conversation.messages.all()[:limit]]
