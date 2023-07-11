import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from RegLog.selectors.users import get_user_by_id
from RegLog.serives.friends import get_user_friend
from .models import Messages
from .selectors.chat import get_chat
from .selectors.message import get_chat_messages
# from .services.message import create_message


# щоб відкрити чат, нам достатньо передавати id друга, свій id ми і так взнаємо
def ChatPage(request, another_user_id):
    user = request.user  # ось в request і так зберігається інфа про те, хто ми
    another_user = get_user_by_id(another_user_id)
    friends = get_user_friend(user, another_user)

    if not friends:
        return redirect('home')

    chat = get_chat(friends)
    context = {
        'All_Messages': get_chat_messages(chat),
        'room_name_json': mark_safe(json.dumps(chat.get_name_room()))
    }

    # if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
    #     message = request.POST.get('message')
    #     create_message(chat, message)

    return render(request, 'chat/ChatHTML.html', context)


def DeleteMessage(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        delete_message = request.POST.get('message_id')
        delete_message_bd = Messages.objects.get(id=delete_message)
        delete_message_bd.delete()
    return JsonResponse({'status': 'success'})
