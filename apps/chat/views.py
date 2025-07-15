from rest_framework.views import APIView
from rest_framework.response import Response
from apps.chat.models import Conversation, ConversationMessage
from apps.chat.serializers import ConversationSerializer


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
                serializer = ConversationSerializer(conversation)
                return Response(serializer.data, status=200)
            except Conversation.DoesNotExist:
                return Response({"error": "Conversation not found"}, status=404)
        else:
            conversation = Conversation.objects.create()
            serializer = ConversationSerializer(conversation)
            return Response(serializer.data, status=200)
