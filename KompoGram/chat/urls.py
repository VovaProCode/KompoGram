from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:user1_id>-<int:user2_id>', views.ChatPage, name='ChatId'),
    path('delete-message/', views.DeleteMessage, name='DeleteMessage')
]