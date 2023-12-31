import base64
import json
from django.core.files.base import ContentFile
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from RegLog.selectors.users import get_user_by_id_async
from RegLog.serives.friends import get_user_friend_async
from .models import Messages
from .selectors.chat import get_chat_async, chat_online_async, chat_offline_async
from chat.services.message import create_message_async, delete_message_async, get_messages_by_id_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        first_user_id, second_user_id = await self.get_to_user_from_url()
        if first_user_id == user.id:
            to_user_id = second_user_id
        else:
            to_user_id = first_user_id
        to_user = await get_user_by_id_async(to_user_id)
        friends = await get_user_friend_async(user, to_user)
        await chat_online_async(friends, user, to_user)
        chat = await get_chat_async(friends)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print('dissss')
        user = self.scope['user']
        first_user_id, second_user_id = await self.get_to_user_from_url()
        if first_user_id == user.id:
            to_user_id = second_user_id
        else:
            to_user_id = first_user_id
        to_user = await get_user_by_id_async(to_user_id)
        friends = await get_user_friend_async(user, to_user)
        await chat_offline_async(friends, user, to_user)
        chat = await get_chat_async(friends)
        print(chat.user1_is_online)
        print(chat.user2_is_online)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        event_type = text_data_json['type']
        if event_type == 'send_message':
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

            message = await create_message_async(chat, message_text, user, reply=None, picture=None, video=None)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'new_message',
                    'user': username,
                    'to_user': to_user.username,
                    'message': message_text,
                    'id': message.id,
                    'picture_profile': message.created_by.picture.url
                }
            )
        elif event_type == 'new_message_reply':
            print("is ok")
            message_text = text_data_json['message_text']
            reply_message_id = text_data_json['to_reply']
            print(text_data_json)
            print(reply_message_id)
            reply = await get_messages_by_id_async(reply_message_id)
            print(reply.message)
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

            message = await create_message_async(chat, message_text, user, reply, picture=None, video=None)

            if not reply.message:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'send_message_reply',
                        'user': username,
                        'to_user': to_user.username,
                        'message': message_text,
                        'id': message.id,
                        'picture_profile': message.created_by.picture.url,
                        'reply_to_message_text': reply.picture.url,
                        'reply_is_picture': 'yes'
                    }
                )
            else:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'send_message_reply',
                        'user': username,
                        'to_user': to_user.username,
                        'message': message_text,
                        'id': message.id,
                        'picture_profile': message.created_by.picture.url,
                        'reply_to_message_text': reply.message,
                        'reply_is_picture': 'no'
                    }
                )
        elif event_type == 'delete_message':
            message_id = text_data_json['message_id']
            await delete_message_async(message_id)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'delete_message',
                    'message_id': message_id,
                }
            )

        elif event_type == 'send_photo':
            photo = text_data_json['photo']
            format, imgstr = photo.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
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
            if ext == 'mp4':
                message = await create_message_async(chat, message=None, created_by=user, reply=None, picture=None,
                                                     video=data)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'new_photo',
                        'user': username,
                        'to_user': to_user.username,
                        'photo': message.video.url,
                        'id': message.id,
                        'picture_profile': message.created_by.picture.url,
                        'is_video': 'yes'
                    }
                )
            else:
                message = await create_message_async(chat, message=None, created_by=user, reply=None, picture=data,
                                                     video=None)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'new_photo',
                        'user': username,
                        'to_user': to_user.username,
                        'photo': message.picture.url,
                        'id': message.id,
                        'picture_profile': message.created_by.picture.url,
                        'is_video': 'no'
                    }
                )

        elif event_type == 'new_message_reply_picture':
            photo = text_data_json['photo_reply']
            format, imgstr = photo.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            reply_message_id = text_data_json['to_reply']
            reply = await get_messages_by_id_async(reply_message_id)
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

            message = await create_message_async(chat, message=None, created_by=user, reply=reply, picture=data, video=None)

            if not reply.message:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'send_message_reply_picture',
                        'user': username,
                        'to_user': to_user.username,
                        'photo': message.picture.url,
                        'id': message.id,
                        'picture_profile': message.created_by.picture.url,
                        'reply_to_message_text': reply.picture.url,
                        'reply_is_picture': 'yes'
                    }
                )
            else:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'send_message_reply_picture',
                        'user': username,
                        'to_user': to_user.username,
                        'photo': message.picture.url,
                        'id': message.id,
                        'picture_profile': message.created_by.picture.url,
                        'reply_to_message_text': reply.message,
                        'reply_is_picture': 'no'
                    }
                )

    async def new_message(self, event):
        user = event['user']
        to_user = event['to_user']
        message_text = event['message']
        id = event['id']
        picture_profile = event['picture_profile']

        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'user': user,
            'to_user': to_user,
            'message': message_text,
            'id': id,
            'picture_profile': picture_profile
        }))

    async def delete_message(self, event):
        message_id = event['message_id']
        await self.send(text_data=json.dumps({
            'type': 'delete_message',
            'message_id': message_id,
        }))

    async def send_message_reply(self, event):
        user = event['user']
        to_user = event['to_user']
        message_text = event['message']
        id = event['id']
        picture_profile = event['picture_profile']
        reply = event['reply_to_message_text']
        is_picture = event['reply_is_picture']

        await self.send(text_data=json.dumps({
            'type': 'send_message_reply',
            'user': user,
            'to_user': to_user,
            'message': message_text,
            'id': id,
            'picture_profile': picture_profile,
            'reply_to_message_text': reply,
            'reply_is_picture': is_picture
        }))

    async def new_photo(self, event):
        user = event['user']
        to_user = event['to_user']
        photo = event['photo']
        id = event['id']
        picture_profile = event['picture_profile']
        is_photo = event['is_video']

        await self.send(text_data=json.dumps({
            'type': 'new_photo',
            'user': user,
            'to_user': to_user,
            'photo': photo,
            'id': id,
            'picture_profile': picture_profile,
            'is_photo': is_photo
        }))
    async def send_message_reply_picture(self, event):
        user = event['user']
        to_user = event['to_user']
        photo = event['photo']
        id = event['id']
        picture_profile = event['picture_profile']
        reply = event['reply_to_message_text']
        reply_is_picture = event['reply_is_picture']

        await self.send(text_data=json.dumps({
            'type': 'send_message_reply_picture',
            'user': user,
            'to_user': to_user,
            'photo': photo,
            'id': id,
            'picture_profile': picture_profile,
            'reply_to_message_text': reply,
            'reply_is_picture': reply_is_picture,
        }))

    async def get_to_user_from_url(self):
        path = self.scope['path']
        print(path)
        parts = path.split('/')
        temp = parts[-2].split('_')
        temp = list(map(int, temp))
        print(temp)
        return temp

    @sync_to_async
    def get_id_bd(self):
        id_message = Messages.objects.count()
        count = id_message + 1
        return count

class HomeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['home_name']
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
        # Обработка данных от клиента
        text_data_json = json.loads(text_data)
        event_type = text_data_json['type']
        if event_type == 'new_message?':
            user = self.scope['user']
            message = text_data_json['message']
            to_user_offline = await self.get_to_user_from_url()
            to_user = await get_user_by_id_async(to_user_offline)
            friends = await get_user_friend_async(user, to_user)
            chat = await get_chat_async(friends)
            print(chat.user1_is_online)
            print(chat.user2_is_online)
            if to_user_offline > user.id:
                if not chat.user2_is_online:
                    print('дааааааа')
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'add_new_message_offline',
                            'from_user': user.username,
                            'message': message
                        }
                    )
            else:
                if not chat.user1_is_online:
                    print('дааааааа')
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'add_new_message_offline',
                            'from_user': user.username,
                            'message': message
                        }
                    )

    async def add_new_message_offline(self, event):
        typee = event['type']
        from_user = event['from_user']
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': typee,
            'from_user': from_user,
            'message': message
        }))

    async def get_to_user_from_url(self):
        path = self.scope['path']
        parts = path.split('/')
        temp = parts[-2].split('_')
        temp = temp[1]
        return int(temp)