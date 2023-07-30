from asgiref.sync import sync_to_async

from chat.models import Messages


def create_message(chat, message, created_by, reply, picture):
    return Messages.objects.create(chat=chat, message=message, created_by=created_by, reply=reply, picture=picture)

async def create_message_async(chat, message, created_by, reply, picture):
    return await sync_to_async(create_message, thread_sensitive=True)(chat, message, created_by, reply, picture)

def get_message_by_id(id):
    return Messages.objects.get(id=id)

async def get_messages_by_id_async(id):
    return await sync_to_async(get_message_by_id, thread_sensitive=True)(id)

def delete_message(id):
    temp = Messages.objects.filter(id=id)
    return temp.delete()

async def delete_message_async(id):
    return await sync_to_async(delete_message, thread_sensitive=True)(id)