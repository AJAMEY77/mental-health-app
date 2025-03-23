# Create a new file: resources/recommendations.py
from .models import Resource, SelfHelpExercise
from chatbot.models import Conversation
from mood_tracker.models import MoodEntry
from collections import Counter

def get_personalized_recommendations(user, limit=3):
    """Generate personalized resource recommendations based on user interactions"""
    # Get recent conversations
    recent_convos = Conversation.objects.filter(user=user).order_by('-timestamp')[:20]
    
    # Extract user messages
    user_messages = ' '.join([convo.user_message for convo in recent_convos])
    
    # Get recent mood entries
    mood_entries = MoodEntry.objects.filter(user=user).order_by('-timestamp')[:10]
    
    # Calculate average mood
    if mood_entries:
        avg_mood = sum(entry.mood_score for entry in mood_entries) / len(mood_entries)
    else:
        avg_mood = 3  # Default to neutral
    
    # Define keywords for different categories
    category_keywords = {
        'anxiety': ['anxious', 'nervous', 'worry', 'panic', 'fear', 'stress'],
        'depression': ['sad', 'depressed', 'hopeless', 'empty', 'worthless'],
        'stress': ['overwhelmed', 'pressure', 'tense', 'burnout', 'exhausted'],
        'general': ['wellbeing', 'mental health', 'self-care', 'balance', 'mindful'],
        'crisis': ['emergency', 'crisis', 'urgent', 'suicide', 'harm']
    }
    
    # Count occurrences of each category's keywords
    category_counts = Counter()
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            count = user_messages.lower().count(keyword)
            category_counts[category] += count
    
    # Adjust based on mood
    if avg_mood <= 2:  # Bad mood
        category_counts['depression'] += 3
        category_counts['crisis'] += 1
    elif avg_mood <= 3:  # Neutral mood
        category_counts['general'] += 2
        category_counts['stress'] += 1
    
    # Get top categories
    top_categories = [category for category, _ in category_counts.most_common(2)]
    
    # If no strong signals, default to general
    if not top_categories:
        top_categories = ['general']
    
    # Get resources for top categories
    recommended_resources = Resource.objects.filter(category__in=top_categories)[:limit]
    
    # Get exercises for top categories
    recommended_exercises = SelfHelpExercise.objects.filter(category__in=top_categories)[:limit]
    
    return {
        'resources': recommended_resources,
        'exercises': recommended_exercises,
        'top_categories': top_categories
    }