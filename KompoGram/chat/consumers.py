import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Messages

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
        message = text_data_json['message']
        user = self.scope['user'].username
        to_user = self.get_to_user_from_url()
        id = await self.get_id_bd()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user': user,
                'to_user': to_user,
                'message': message,
                'id': id
            }
        )

    async def chat_message(self, event):
        user = event['user']
        to_user = event['to_user']
        message = event['message']
        id = event['id']

        await self.send(text_data=json.dumps({
            'type': 'chat',
            'user': user,
            'to_user': to_user,
            'message': message,
            'id': id
        }))

    def get_to_user_from_url(self):
        # Получаем имя пользователя из URL-адреса
        path = self.scope['path']
        parts = path.split('/')
        username = parts[-1] if parts[-1] else parts[-2]
        return username

    @sync_to_async
    def get_id_bd(self):
        id_message = Messages.objects.count()
        count = id_message + 1
        return count