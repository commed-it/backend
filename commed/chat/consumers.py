import json
import uuid

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from chat.models import Message
from offer.models import Encounter


class ChatConsumer(AsyncJsonWebsocketConsumer):
    room_group_name: str
    room_name: str
    encounter: Encounter

    async def connect(self):
        # username = self.scope["user"].username
        # Put on else if not wanted
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        try:
            uuid_room = uuid.UUID(self.room_name)
            self.encounter = await self.get_encounter_from_db(uuid_room)
            await self._create_connection()
        except ValueError:
            await self.close('UUID is not valid')
        except Encounter.DoesNotExist:
            await self.close('Encounter page does not exist')

        # User is not connected if username == ''
        # Now I don't really care about it, as it makes it hard to debug
        # if username == '':
        # await self.close('User is not authenticated')

    @database_sync_to_async
    def get_encounter_from_db(self, uuid_room):
        return Encounter.objects.get(id=uuid_room)

    async def _create_connection(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive_json(self, content):
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': content
            }
        )

    @database_sync_to_async
    def create_message(self, sender_username: str, msg: str, context: Encounter):
        new_msg = Message.objects.create(  # author=sender,
            msg=msg, channel_context=context)
        new_msg.save()
        return new_msg

    # Receive message from room group
    async def chat_message(self, event):
        username = self.scope["user"].username
        message = event['message']
        _ = await self.create_message(username, message, self.encounter)
        # message = { "message": content } already, so there is no need to parse it
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
