from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('<str:user1>-<str:user2>', views.ChatPage, name='ChatId'),
    path('delete-message/', views.DeleteMessage, name='DeleteMessage')
]