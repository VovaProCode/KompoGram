from django.db.models import Q

from RegLog.models import Friends
from RegLog.serives.friends import get_user_friend
from chat.selectors.chat import get_chat
from chat.selectors.message import get_chat_messages_none_time


def get_friends(user):
    friends = []
    temp_friends = Friends.objects.filter(Q(first_user=user) | Q(second_user=user))
    for i in temp_friends:
        if user == i.first_user:
            friends.append(i.second_user)
        if user == i.second_user:
            friends.append(i.first_user)
    return friends

def get_friends_and_friend_message(user):
    friends_and_messages = []
    friends = []
    temp_friends = Friends.objects.filter(Q(first_user=user) | Q(second_user=user))
    for i in temp_friends:
        if user == i.first_user:
            friends.append(i.second_user)
        if user == i.second_user:
            friends.append(i.first_user)
    print(friends)
    for friend in friends:
        Friends1 = get_user_friend(user, friend)
        chat = get_chat(Friends1)
        all_friends_messages = get_chat_messages_none_time(chat)
        print(all_friends_messages)
        if not all_friends_messages:
            print("No first message")
            friends_and_messages.append([friend, None])
        else:
            friends_and_messages.append([friend, all_friends_messages.last()])

    print(friends_and_messages)

    return friends_and_messages
