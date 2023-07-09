from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass

class Friends(models.Model):
    first_user = models.ForeignKey(CustomUser, related_name='first_user', on_delete=models.CASCADE)
    second_user = models.ForeignKey(CustomUser, related_name='second_user', on_delete=models.CASCADE)

class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='to_user', on_delete=models.CASCADE)
