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

def chat_online(friends, first_user, second_user):
    chat = get_chat(friends)
    if second_user.id > first_user.id:
        chat.user1_is_online = True
    else:
        chat.user2_is_online = True
    chat.save()

async def chat_online_async(friends, first_user, second_user):
    return await sync_to_async(chat_online, thread_sensitive=True)(friends, first_user, second_user)

def chat_offline(friends, first_user, second_user):
    chat = get_chat(friends)
    print('ofline chat')
    if second_user.id > first_user.id:
        print('bbbbbbbb')
        chat.user1_is_online = False
    else:
        chat.user2_is_online = False
        print('bbbbbabbb')
    chat.save()

async def chat_offline_async(friends, first_user, second_user):
    return await sync_to_async(chat_offline, thread_sensitive=True)(friends, first_user, second_user)
