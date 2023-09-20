from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomePage, name='home'),
    path('account/', views.AccountPage, name='account'),
]