from rest_framework.views import APIView
from rest_framework.response import Response
from apps.chat.models import Conversation
from apps.chat.serializers import ConversationSerializer


from apps.chat.engines.ollama_engine import OllamaChatEngine
from apps.chat.services.debate import DebateService
from apps.chat.services.conversation import ConversationService


class ConversationView(APIView):

    def post(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation_id", None)
        message_text = request.data.get("message")

        if not message_text:
            return Response({"error": "Message is required."}, status=400)

        conversation_service = ConversationService()
        debate_service = DebateService(OllamaChatEngine())

        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
            except Conversation.DoesNotExist:
                return Response({"error": "Conversation not found"}, status=404)

            conversation_service.add_message(conversation, message_text, rol="user")

        else:
            conversation = conversation_service.create_conversation(message_text=message_text)

        last_messages = conversation_service.get_last_messages(conversation, limit=5)
        bot_reply = debate_service.handle_turn(
            topic=conversation.topic,
            messages=last_messages,
        )

        conversation_service.add_message(conversation, bot_reply, rol="bot")

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=200)
