from asgiref.sync import sync_to_async

from RegLog.models import CustomUser


def get_user_by_id(user_id):
    return CustomUser.objects.filter(id=user_id).first()

async def get_user_by_id_async(user_id):
    return await sync_to_async(get_user_by_id, thread_sensitive=True)(user_id)