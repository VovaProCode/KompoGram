from django.db import models

# Create your models here.

class Messages(models.Model):
    chat = models.CharField("Чат:", max_length=100)
    from_user = models.CharField("Повідомлення від:", max_length=100, blank=True, null=True)
    message = models.TextField('Повідомлення')
    time = models.TimeField('Час відправки:')
    id_message = models.CharField('Id-шник', max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.chat