from asgiref.sync import sync_to_async

from chat.models import Messages


def create_message(chat, message, created_by):
    return Messages.objects.create(chat=chat, message=message, created_by=created_by)

async def create_message_async(chat, message, created_by):
    return await sync_to_async(create_message, thread_sensitive=True)(chat, message, created_by)

def delete_message(id):
    temp = Messages.objects.get(id=id)
    return temp.delete()

async def delete_message_async(id):
    return await sync_to_async(delete_message, thread_sensitive=True)(id)