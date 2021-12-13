import json
import uuid
import collections as c

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import User

from chat.models import Message
from enterprise.models import Enterprise
from offer.models import Encounter



class ChatConsumer(AsyncJsonWebsocketConsumer):
    room_group_name: str
    room_name: str
    encounter: Encounter
    user: User

    async def connect(self):
        # Put on else if not wanted
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        try:
            uuid_room = uuid.UUID(self.room_name)
            self.encounter = await self.get_encounter_from_db(uuid_room)
            await self._create_connection()
        except ValueError:
            await self.close('UUID is not valid')
        except Encounter.DoesNotExist:
            await self.close('Encounter page does not exist')
        except User.DoesNotExist:
            await self.close('User does not exist. How did this happen?')

    @database_sync_to_async
    def get_user_from_db(self, user_id):
        return User.objects.get(pk=user_id)

    @database_sync_to_async
    def get_encounter_from_db(self, uuid_room):
        return Encounter.objects.get(id=uuid_room)

    async def _create_connection(self):
        # Join room group
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
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
    async def receive_json(self, content, **kwargs):
        """
        content = TextMessage {
        , user :: Int
        , text :: String
        } | E

        """
        # Send message to room group
        # Check
        user = await self.get_user_from_db(content['user'])
        _ = await self.create_message(user, content['text'], self.encounter)
        parsed_message = json.loads(content["message"])
        if is_the_message_correct(parsed_message):
            print("An error has occurred while parsing the data. Please check that the client is correct")
            print(f"data={content}, parsed_message={parsed_message}")
            return None
        user = await self.get_user_from_db(parsed_message['user'])
        _ = await self.create_message(user, content, self.encounter)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': content['text']
            }
        )

    @database_sync_to_async
    def create_message(self, sender: User, msg: str, context: Encounter):
        new_msg = Message.objects.create(author=sender,
                                         msg=msg, channel_context=context)
        new_msg.save()
        return new_msg

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # message = { "message": content } already, so there is no need to parse it
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))


def is_the_message_correct(a_dict: dict) -> bool:
    a = c.defaultdict(lambda: lambda _:False)
    a['message'] = lambda x: 'message' in x and type(x['message']) == str
    a['formalOffer'] = lambda x: 'formalOffer' in x and type(x['formalOffer']) == int
    return 'type' in a_dict and a[a_dict['type']](a_dict)

