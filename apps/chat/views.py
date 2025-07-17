from rest_framework.views import APIView
from rest_framework.response import Response
from apps.chat.models import Conversation, ConversationMessage
from apps.chat.serializers import ConversationSerializer

from apps.chat.engines.ollama_engine import OllamaChatEngine
from apps.chat.services.debate import DebateService


class ConversationView(APIView):

    def post(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation_id", None)
        message = request.data.get("message", None)
        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
                ConversationMessage.objects.create(
                    conversation=conversation, rol="user", message=message
                )

                response = DebateService(OllamaChatEngine()).handle_turn(
                    topic=conversation.topic,
                    messages=[
                        {"rol": message.rol, "message": message.message}
                        for message in conversation.messages.all()
                    ],
                )
                ConversationMessage.objects.create(
                    conversation=conversation, rol="bot", message=response
                )
                serializer = ConversationSerializer(conversation)
                return Response(serializer.data, status=200)
            except Conversation.DoesNotExist:
                return Response({"error": "Conversation not found"}, status=404)
        else:
            conversation = Conversation.objects.create(topic=message)
            serializer = ConversationSerializer(conversation)
            return Response(serializer.data, status=200)
