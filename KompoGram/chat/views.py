import datetime

from django.http import JsonResponse
from django.shortcuts import render
# from RegLog.models import CustomUser
from .models import Messages


# Create your views here.

def ChatPage(request, username):
    from_user = request.user.username
    to_user = request.path
    to_user = to_user.split('/')
    to_user = to_user[-1]
    Otpravka = Messages.objects.filter(from_user=from_user, to_user=to_user)
    Get = Messages.objects.filter(from_user=to_user, to_user=from_user)
    context = {'Otpravka': Otpravka, 'Get': Get}
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        message = request.POST.get('message')
        print(message)
        print("asdfDSFJSDFJSDFJDSAFDSFDSSSSSSSSSSSSSSSSSSS")
        from_user = request.user.username
        to_user = request.path
        print(to_user)
        to_user = to_user.split('/')
        to_user = to_user[-1]
        print(to_user)
        Message = Messages.objects.get_or_create(from_user=from_user, to_user=to_user, message=message, time=datetime.time)
        return JsonResponse({'success': True})
    return render(request, 'chat/ChatHTML.html', context)