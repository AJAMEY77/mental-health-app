import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import base64

# Download NLTK resources
nltk.download('vader_lexicon')

def analyze_text_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)
    
    # Map compound score to mood scale (1-5)
    compound = sentiment_score['compound']
    if compound <= -0.6:
        return 1  # Very Bad
    elif compound <= -0.2:
        return 2  # Bad
    elif compound <= 0.2:
        return 3  # Neutral
    elif compound <= 0.6:
        return 4  # Good
    else:
        return 5  # Very Good

def generate_mood_chart(user):
    # Get user's mood entries
    from mood_tracker.models import MoodEntry
    entries = MoodEntry.objects.filter(user=user).order_by('timestamp')
    
    if not entries:
        return None
    
    # Convert to DataFrame
    data = {
        'date': [entry.timestamp.date() for entry in entries],
        'mood': [entry.mood_score for entry in entries]
    }
    df = pd.DataFrame(data)
    
    # Group by date (in case multiple entries per day)
    daily_mood = df.groupby('date')['mood'].mean().reset_index()
    
    # Create plot
    plt.figure(figsize=(10, 6))
    plt.plot(daily_mood['date'], daily_mood['mood'], marker='o')
    plt.title('Your Mood Over Time')
    plt.xlabel('Date')
    plt.ylabel('Mood (1-5)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.ylim(0.5, 5.5)
    plt.yticks([1, 2, 3, 4, 5], ['Very Bad', 'Bad', 'Neutral', 'Good', 'Very Good'])
    
    # Save to BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    # Encode to base64 for embedding in HTML
    return base64.b64encode(image_png).decode('utf-8')