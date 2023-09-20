import json
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from RegLog.selectors.users import get_user_by_id
from RegLog.serives.friends import get_user_friend
from .models import Messages
from .selectors.chat import get_chat
from .selectors.message import get_chat_messages
from chat.services.stream_video import open_file


# from .services.message import create_message


# щоб відкрити чат, нам достатньо передавати id друга, свій id ми і так взнаємо
def ChatPage(request, another_user_id):
    if not request.user.is_authenticated:
        return redirect('registration')
    user = request.user  # ось в request і так зберігається інфа про те, хто ми
    another_user = get_user_by_id(another_user_id)
    home_room = f'_{another_user_id}_'
    friends = get_user_friend(user, another_user)

    if not friends:
        return redirect('home')

    chat = get_chat(friends)
    context = {
        'All_Messages': get_chat_messages(chat),
        'room_name_json': mark_safe(json.dumps(chat.get_name_room())),
        'home_name_json': mark_safe(json.dumps(home_room)),
        'my_name_json': mark_safe(json.dumps(f'_{user.id}_'))
    }

    # if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
    #     message = request.POST.get('message')
    #     create_message(chat, message, user)

    return render(request, 'chat/ChatHTML.html', context)


def DeleteMessage(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        delete_message = request.POST.get('message_id')
        delete_message_bd = Messages.objects.get(id=delete_message)
        delete_message_bd.delete()
    return JsonResponse({'status': 'success'})

def get_streaming_video(request, id):
    file, status_code, content_length, content_range = open_file(request, id)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range

    return response
