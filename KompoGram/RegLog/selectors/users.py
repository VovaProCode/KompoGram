from RegLog.models import CustomUser


def get_user_by_id(user_id):
    return CustomUser.objects.filter(id=user_id).first()