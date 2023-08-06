from chat.models import Messages


def get_chat_messages(chat):
    return Messages.objects.filter(chat=chat).order_by("time")

def get_chat_messages_none_time(chat):
    return Messages.objects.filter(chat=chat)