from django.urls import path, include
from . import views
from .views import SendRequest, AcceptRequest

urlpatterns = [
    path('registration', views.RegistrationPage, name='registration'),
    path('login', views.LoginPage, name="login"),
    path('logout', views.LogoutPage, name='logout'),
    path('search/', views.SearchUsers, name='search_qqq'),
    path('add-friend/<int:id>/', SendRequest, name='add-friend'),
    path('accept/<int:id>', AcceptRequest, name='accept'),
]
