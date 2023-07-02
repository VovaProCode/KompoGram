import json
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

# from RegLog.models import CustomUser
from .models import Messages


# Create your views here.

def ChatPage(request, user1, user2):
    friends = request.user.friends.filter(username=user1)
    if not friends.exists():
        return redirect('home')
    else:
        current_time = datetime.now().time()
        if user1 > user2:
            user_more = user2 + '_' + user1
        elif user2 > user1:
            user_more = user1 + '_' + user2
        chat_messages = Messages.objects.filter(chat=user_more).order_by("time")
        context = {'All_Messages': chat_messages, 'room_name_json': mark_safe(json.dumps(user_more))}
        if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            message = request.POST.get('message')
            from_user = request.user.username
            all_messages = Messages.objects.count()
            count = all_messages + 1
            Message = Messages.objects.get_or_create(chat=user_more, from_user=from_user,
                                                     message=message, time=current_time,
                                                     id_message=count)
    return render(request, 'chat/ChatHTML.html', context)

def DeleteMessage(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        delete_message = request.POST.get('message_id')
        delete_message_bd = Messages.objects.get(id_message=delete_message)
        delete_message_bd.delete()
    return JsonResponse({'status': 'success'})