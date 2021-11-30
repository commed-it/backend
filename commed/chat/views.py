import uuid

from django.shortcuts import render

from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny

from chat.models import Message
from chat.serializers import MessageSerializer
from offer.models import Encounter


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


class MessageViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for interacting with Enterprises
    """
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        try:
            encounter_uuid = self.kwargs['encounter_uuid']
            parsed_uuid = uuid.UUID(encounter_uuid)
            encounter = Encounter.objects.get(id=parsed_uuid)
            return Message.objects.filter(channel_context=encounter).order_by('-timestamp')
        except: # All errors should return None
            return Message.objects.none()

