from chat.models import Messages


def get_chat_messages(chat):
    return Messages.objects.filter(chat=chat).order_by("time")