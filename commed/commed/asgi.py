"""
ASGI config for commed project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""
import os
import django
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "commed.settings")
django.setup()

def create_application():
    import chat.routing
    return ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                path("ws/chat/", URLRouter(chat.routing.websocket_urls), name="websocket-chat"),
            ]
        )

    )
})
