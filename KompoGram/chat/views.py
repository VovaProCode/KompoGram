from django.shortcuts import render
from RegLog.models import CustomUser


# Create your views here.

def ChatPage(request, username):
    users = CustomUser.objects.filter(username=username)
    return render(request, 'chat/ChatHTML.html')