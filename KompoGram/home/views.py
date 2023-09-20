import json
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from RegLog.models import FriendRequest, CustomUser
from RegLog.selectors.friends import get_friends, get_friends_and_friend_message
from RegLog.selectors.users import get_user_by_id
from RegLog.serives.friends import get_user_friend
from chat.selectors.chat import get_chat


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
        user = request.user
        context = {"username": username, 'email': email,"users": users,
                   'friends_requests': friends_requests, 'friends': last_messages_and_friends,
                   'home_name_json': mark_safe(json.dumps(f'_{user.id}_'))}
        return render(request, 'home/HomeHTML.html', context)

def AccountPage(request):
    user = request.user
    context = {'error': '',
               'home_name_json': mark_safe(json.dumps(f'_{user.id}_'))}
    if not request.user.is_authenticated:
        return redirect('registration')
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password_confirm = request.POST.get('new_password_confirm')
        this_user = request.user
        all_users = CustomUser.objects.all()
        users_username = []
        error = ''
        if not new_name:
            this_user.username = this_user.username
        else:
            for i in all_users:
                users_username.append(i.username)
                print(users_username)
            if new_name in users_username:
                this_user.username = this_user.username
                error = 'Таке ім`я вже є'
            else:
                this_user.username = new_name
        new_picture = request.FILES.get('new_picture')
        if new_picture:
            this_user.picture = new_picture
        else:
            this_user.picture = this_user.picture
        if old_password and new_password and new_password_confirm:
            if this_user.check_password(old_password):
                if new_password == new_password_confirm:
                    this_user.set_password(new_password)
                else:
                    error = 'Паролі не одинакові'
            else:
                error = 'Теперішній пароль не зівпадає в вашим'
        this_user.save()
        context = {'error': error,
                   'home_name_json': mark_safe(json.dumps(f'_{this_user.id}_'))}
    return render(request, 'home/AccountHTML.html', context)
