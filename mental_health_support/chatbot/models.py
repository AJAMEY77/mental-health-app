# chatbot/models.py
from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_message = models.TextField()
    bot_response = models.TextField()
    
    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"



