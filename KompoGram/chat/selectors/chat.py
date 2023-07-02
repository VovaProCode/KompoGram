from chat.models import Chat
from django.contrib.auth import get_user_model

def get_chat(first_user_id, second_user_id):
    if first_user_id > second_user_id:
        temp = first_user_id
        first_user_id = second_user_id
        second_user_id = temp
    
    user1 = get_user_model().objects.get(id=first_user_id)
    user2 = get_user_model().objects.get(id=second_user_id)
    return Chat.objects.get_or_create(firts_user=user1, second_user=user2)
