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

# mood_tracker/models.py
class MoodEntry(models.Model):
    MOOD_CHOICES = [
        (1, 'Very Bad'),
        (2, 'Bad'),
        (3, 'Neutral'),
        (4, 'Good'),
        (5, 'Very Good'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    mood_score = models.IntegerField(choices=MOOD_CHOICES)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.mood_score} - {self.timestamp}"

# resources/models.py
class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('anxiety', 'Anxiety'),
        ('depression', 'Depression'),
        ('stress', 'Stress'),
        ('general', 'General Wellbeing'),
        ('crisis', 'Crisis Support'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
    def __str__(self):
        return self.title

class SelfHelpExercise(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField()
    category = models.CharField(max_length=50, choices=Resource.CATEGORY_CHOICES)
    
    def __str__(self):
        return self.title