from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from RegLog.models import FriendRequest, CustomUser
from RegLog.selectors.friends import get_friends


# Create your views here.

def HomePage(request):
    if not request.user.is_authenticated:
        return redirect('registration')
    else:
        username = request.user.username
        email = request.user.email
        users = CustomUser.objects.exclude(username='admin')
        friends_requests = FriendRequest.objects.filter(to_user=request.user)
        friends = get_friends(request.user)
        context = {"username": username, 'email': email,"users": users,
                   'friends_requests': friends_requests, 'friends': friends}
        return render(request, 'home/HomeHTML.html', context)

def AccountPage(request):
    return render(request, 'home/AccountHTML.html')

def ChangeName(request):
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        this_user = request.user
        this_user.username = new_name
        this_user.save()