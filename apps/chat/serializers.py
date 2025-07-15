from typing import List

from rest_framework import serializers
from apps.chat.models import Conversation, ConversationMessage


class ConversationMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationMessage
        fields = [
            "rol",
            "message",
        ]


class ConversationSerializer(serializers.ModelSerializer):

    conversation_id = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ["conversation_id", "message"]

    def get_conversation_id(self, obj):
        return obj.id

    def get_message(self, obj) -> List:
        return ConversationMessageSerializer(obj.messages.all()[:5], many=True).data

    def create(self, validated_data):
        message_data = validated_data.pop("message", [])
        conversation = Conversation.objects.create(**validated_data)

        for message_data in message_data:
            ConversationMessage.objects.create(conversation=conversation, **message_data)

        return conversation
