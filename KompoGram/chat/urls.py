from django.urls import path
from . import views

urlpatterns = [
    path('<int:another_user_id>', views.ChatPage, name='ChatId'),
    path('delete-message/', views.DeleteMessage, name='DeleteMessage'),
    path('stream_video/<int:id>/', views.get_streaming_video, name='stream_video'),
]
