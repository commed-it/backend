from rest_framework import serializers

from chat.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("channel_context", "msg", "timestamp")
