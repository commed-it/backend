from django.contrib.auth.models import User
from django.db import models

from offer.models import Encounter


class Message(models.Model):
    """
    Message Model. It stores the messages in the chat.
    """
    # author = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    channel_context = models.ForeignKey(Encounter, primary_key=False, on_delete=models.CASCADE, editable=False, db_index=True)
    msg = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f'Message(channel_context={self.channel_context}, msg={self.msg}, timestamp={self.timestamp})'
