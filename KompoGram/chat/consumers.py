import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from RegLog.selectors.users import get_user_by_id, get_user_by_id_async
from RegLog.serives.friends import get_user_friend, get_user_friend_async
from .models import Messages
from .selectors.chat import get_chat, get_chat_async
from .services.message import create_message, create_message_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json['message']
        user = self.scope['user']
        username = user.username
        first_user_id, second_user_id = await self.get_to_user_from_url()
        if first_user_id == user.id:
            to_user_id = second_user_id
        else:
            to_user_id = first_user_id
        to_user = await get_user_by_id_async(to_user_id)
        friends = await get_user_friend_async(user, to_user)
        chat = await get_chat_async(friends)
        
        message = await create_message_async(chat, message_text, user)



        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user': username,
                'to_user': to_user.username,
                'message': message_text,
                'id': message.id
            }
        )

    async def chat_message(self, event):
        user = event['user']
        to_user = event['to_user']
        message_text = event['message']
        id = event['id']

        await self.send(text_data=json.dumps({
            'type': 'chat',
            'user': user,
            'to_user': to_user,
            'message': message_text,
            'id': id
        }))

    async def get_to_user_from_url(self):
        path = self.scope['path']
        parts = path.split('/')
        temp = parts[-2].split('_')
        temp = list(map(int, temp))
        return temp

    @sync_to_async
    def get_id_bd(self):
        id_message = Messages.objects.count()
        count = id_message + 1
        return count
