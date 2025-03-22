from django.db import models

# Create your models here.
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
