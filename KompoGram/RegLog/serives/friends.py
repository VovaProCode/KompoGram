from RegLog.models import Friends

def switch_users(first_user, second_user):
    if second_user.id < first_user.id:
        first_user, second_user = second_user, first_user
    return first_user, second_user

def add_friend(first_user, second_user):
    first_user, second_user = switch_users(first_user, second_user)

    return Friends.objects.get_or_create(first_user=first_user, second_user=second_user)[0]

def get_user_friend(first_user, second_user):
    first_user, second_user = switch_users(first_user, second_user)

    return Friends.objects.filter(first_user=first_user, second_user=second_user).first()
