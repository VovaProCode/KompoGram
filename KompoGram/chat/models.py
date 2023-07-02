from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Chat(models.Model):
    firts_user = models.ForeignKey(get_user_model(), related_name='firts_user', on_delete=models.CASCADE)
    second_user = models.ForeignKey(get_user_model(), related_name='second_user', on_delete=models.CASCADE)

    def get_name_room(self):
        return f'{self.firts_user.id}_{self.second_user.id}'

class Messages(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message = models.TextField('Повідомлення')
    time = models.TimeField('Час відправки:')

    def __str__(self):
        return self.chat