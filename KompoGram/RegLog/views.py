import json
import os

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.safestring import mark_safe

from .models import CustomUser, FriendRequest
from .serives.friends import add_friend
from django.core.files import File


# Create your views here.

def RegistrationPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        picture = request.FILES.get('picture')
        if not picture:
            return redirect('home')
        if password1 != password2:
            return redirect('home')
        else:
            user = CustomUser.objects.create_user(username=username, email=email, password=password1, picture=picture)
            user.save()
            user = authenticate(request, username=username, password=password1)
            login(request, user)
            return redirect('home')

    # context = {'form': form}
    return render(request, 'RegLog/RegistrationHTML.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password1')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Pass is wrong')
    return render(request, 'RegLog/LoginHTML.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')
def SearchUsers(request):
    if not request.user.is_authenticated:
        return redirect('registration')
    if request.method == 'POST':
        searched = request.POST["searched"]
        users = CustomUser.objects.filter(username__icontains=searched).exclude(username=request.user.username).exclude(username='admin')
        print(users)
        user = request.user
        context = {"users": users,
                   'home_name_json': mark_safe(json.dumps(f'_{user.id}_'))}
        return render(request, 'RegLog/SearchHTML.html', context)
    elif "term" in request.GET:
        users = User.objects.filter(username__icontains=request.GET.get('term'))
        UsersList = list()
        for i in users:
            UsersList.append(i)
        return JsonResponse(UsersList, safe=False)
    else:
        user = request.user
        context = {'home_name_json': mark_safe(json.dumps(f'_{user.id}_'))}
        return render(request, "RegLog/SearchHTML.html", context)

def SendRequest(request, id):
    from_user = request.user
    to_user = CustomUser.objects.get(id=id)
    friend_request = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
    return redirect('home')
def AcceptRequest(request, id):
    friends_request = FriendRequest.objects.get(id=id)
    user1 = request.user
    user2 = friends_request.from_user
    add_friend(user1, user2)
    friends_request.delete()
    return redirect('home')