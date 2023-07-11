from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, FriendRequest
from .serives.friends import add_friend


# Create your views here.

def RegistrationPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        MyUser = CustomUser.objects.create_user(username, email, password1)
        MyUser.save()
        if password1 != password2:
            return redirect('home')
        else:
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
    if request.method == 'POST':
        searched = request.POST["searched"]
        users = CustomUser.objects.filter(username__icontains=searched).exclude(username='admin')
        context = {"users": users}
        return render(request, 'RegLog/SearchHTML.html', context)
    elif "term" in request.GET:
        users = User.objects.filter(username__icontains=request.GET.get('term'))
        UsersList = list()
        for i in users:
            UsersList.append(i)
        return JsonResponse(UsersList, safe=False)
    else:
        return render(request, "RegLog/SearchHTML.html")

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