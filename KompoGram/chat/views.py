import json
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

# from RegLog.models import CustomUser
from .models import Messages
from .selectors.chat import get_chat

# Create your views here.

def ChatPage(request, user1_id, user2_id):
    friends = request.user.friends.filter(id=user1_id)
    if not friends.exists():
        return redirect('home')
    else:
        current_time = datetime.now().time()
        chat = get_chat(user1_id, user2_id)
        chat_messages = Messages.objects.filter(chat=chat.id).order_by("time")
        context = {'All_Messages': chat_messages, 'room_name_json': mark_safe(json.dumps(chat.get_name_room()))}
        if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            message = request.POST.get('message')
            Messages.objects.get_or_create(chat=chat, message=message, time=current_time)
    return render(request, 'chat/ChatHTML.html', context)

def DeleteMessage(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        delete_message = request.POST.get('message_id')
        delete_message_bd = Messages.objects.get(id_message=delete_message)
        delete_message_bd.delete()
    return JsonResponse({'status': 'success'})