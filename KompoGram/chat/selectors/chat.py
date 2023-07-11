from asgiref.sync import sync_to_async

from chat.models import Chat


def get_chat(friends):
    # проблема була в тому, get_or_create повертає не одне значення, а 2.
    # Перше - об'єкт, який був створений, а друге - чи був об'єкт створений (True або False)
    # друге значення на не треба, тому повертаємо лише перше
    chat, is_created = Chat.objects.get_or_create(friends=friends)
    return chat

async def get_chat_async(friends):
    return await sync_to_async(get_chat, thread_sensitive=True)(friends)
