from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from RegLog.models import FriendRequest, CustomUser
from RegLog.selectors.friends import get_friends, get_friends_and_friend_message
from django.http import JsonResponse

from RegLog.serives.friends import get_user_friend
from chat.selectors.chat import get_chat
from chat.selectors.message import get_chat_messages, get_chat_messages_none_time


# Create your views here.

def HomePage(request):
    if not request.user.is_authenticated:
        return redirect('registration')
    else:
        username = request.user.username
        email = request.user.email
        users = CustomUser.objects.exclude(username='admin')
        friends_requests = FriendRequest.objects.filter(to_user=request.user)
        last_messages_and_friends = get_friends_and_friend_message(request.user)
        context = {"username": username, 'email': email,"users": users,
                   'friends_requests': friends_requests, 'friends': last_messages_and_friends}
        return render(request, 'home/HomeHTML.html', context)

def AccountPage(request):
    if not request.user.is_authenticated:
        return redirect('registration')
    return render(request, 'home/AccountHTML.html')

def ChangeName(request):
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        this_user = request.user
        all_users = CustomUser.objects.all()
        users_username = []
        for i in all_users:
            users_username.append(i.username)
            print(users_username)
        if new_name in users_username:
            this_user.username = this_user.username
        else:
            this_user.username = new_name
        new_picture = request.FILES.get('new_picture')
        if new_picture:
            this_user.picture = new_picture
        else:
            this_user.picture = this_user.picture
        this_user.save()
    return redirect('account')