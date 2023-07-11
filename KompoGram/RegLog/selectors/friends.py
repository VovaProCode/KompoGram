from django.db.models import Q

from RegLog.models import Friends


def get_friends(user):
    friends = []
    temp_friends = Friends.objects.filter(Q(first_user=user) | Q(second_user=user))
    for i in temp_friends:
        if user == i.first_user:
            friends.append(i.second_user)
        if user == i.second_user:
            friends.append(i.first_user)
    return friends