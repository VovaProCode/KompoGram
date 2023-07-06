from chat.models import Chat


def get_chat(first_user, second_user):
    if first_user.id > second_user.id:
        temp = first_user
        first_user = second_user
        second_user = temp

    # проблема була в тому, get_or_create повертає не одне значення, а 2.
    # Перше - об'єкт, який був створений, а друге - чи був об'єкт створений (True або False)
    # друге значення на не треба, тому повертаємо лише перше
    chat, is_created = Chat.objects.get_or_create(firts_user=first_user, second_user=second_user)
    return chat
