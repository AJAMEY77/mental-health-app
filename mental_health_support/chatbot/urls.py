from django.urls import path
from . import views

urlpatterns = [
    path('/api/chatbot/chat/', views.chat_with_bot, name='chat'),
]