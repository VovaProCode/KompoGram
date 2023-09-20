from django.contrib import admin

from .models import FriendRequest, CustomUser, Friends

admin.site.register(FriendRequest)
admin.site.register(CustomUser)
admin.site.register(Friends)