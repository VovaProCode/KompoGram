from django.db import models

# Create your models here.

class Messages(models.Model):
    from_user = models.CharField('Від', max_length=75)
    to_user = models.CharField('Кому', max_length=75)
    message = models.TextField('Повідомлення')
    time = models.TimeField('Час відправки:')

    def __str__(self):
        return self.from_user