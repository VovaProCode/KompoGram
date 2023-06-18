from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from RegLog.models import FriendRequest, CustomUser


# Create your views here.

def HomePage(request):
    if not request.user.is_authenticated:
        return redirect('registration')
    else:
        username = request.user.username
        email = request.user.email
        users = CustomUser.objects.exclude(username='admin')
        friends_requests = FriendRequest.objects.filter(to_user=request.user)
        friends = request.user.friends.exclude(id=request.user.id)
        context = {"username": username, 'email': email,"users": users,
                   'friends_requests': friends_requests, 'friends': friends}
        return render(request, 'home/HomeHTML.html', context)