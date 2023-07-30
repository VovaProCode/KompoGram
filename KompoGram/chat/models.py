import uuid
from django.db import models
from django.contrib.auth import get_user_model
import os
from PIL import Image
from KompoGram import settings
from RegLog.models import Friends
from io import BytesIO
import base64


class Chat(models.Model):
    friends = models.ForeignKey(Friends, on_delete=models.CASCADE)

    def get_name_room(self):
        return f'{self.friends.first_user.id}_{self.friends.second_user.id}'

def image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"image_{uuid.uuid4().hex[:10]}.{ext}"
    return os.path.join('images', filename)
class Messages(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message = models.TextField('Повідомлення', null=True)
    # auto_now_add задає час автоматично при створенні об'єкта
    # DateTimeField краще використовувати, адже тобі треба зберігати і дату відправки
    time = models.DateTimeField(auto_now_add=True, verbose_name='Час відправки:')
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    picture = models.ImageField('Картинка повідомлення', upload_to=image_upload_path, null=True, blank=True)

    def __str__(self):
        if self.message != None:
            return self.message
        else:
            return "picture"
    
