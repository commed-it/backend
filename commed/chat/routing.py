from django.urls import path

from . import consumers

websocket_urls = [
    path("<str:room_name>/", consumers.ChatConsumer.as_asgi())
]

