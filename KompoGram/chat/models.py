from django.db import models
from django.contrib.auth import get_user_model

from RegLog.models import Friends


class Chat(models.Model):
    friends = models.ForeignKey(Friends, on_delete=models.CASCADE)

    def get_name_room(self):
        return f'{self.friends.first_user.id}_{self.friends.second_user.id}'


class Messages(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message = models.TextField('Повідомлення')
    # auto_now_add задає час автоматично при створенні об'єкта
    # DateTimeField краще використовувати, адже тобі треба зберігати і дату відправки
    time = models.DateTimeField(auto_now_add=True, verbose_name='Час відправки:')
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.chat
    
