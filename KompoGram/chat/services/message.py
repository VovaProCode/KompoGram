from chat.models import Messages


def create_message(chat, message):
    Messages.objects.create(chat=chat, message=message)