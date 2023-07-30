from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        picture = extra_fields.pop('picture', None)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)

        if picture:
            user.picture = picture

        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        return self.create_user(username, email, password, **extra_fields)
    
class CustomUser(AbstractUser):
    picture = models.ImageField('Аватарка', upload_to='profile_pictures')

    objects = CustomUserManager()

class Friends(models.Model):
    first_user = models.ForeignKey(CustomUser, related_name='first_user', on_delete=models.CASCADE)
    second_user = models.ForeignKey(CustomUser, related_name='second_user', on_delete=models.CASCADE)

class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='to_user', on_delete=models.CASCADE)
