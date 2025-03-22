from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import MoodEntry
from .utils import analyze_text_sentiment, generate_mood_chart

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def log_mood(request):
    # Direct mood entry
    if 'mood_score' in request.data:
        mood_score = int(request.data.get('mood_score'))
        notes = request.data.get('notes', '')
    # Text analysis for mood
    elif 'text' in request.data:
        text = request.data.get('text')
        mood_score = analyze_text_sentiment(text)
        notes = text
    else:
        return Response(
            {'error': 'Either mood_score or text is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Save mood entry
    entry = MoodEntry.objects.create(
        user=request.user,
        mood_score=mood_score,
        notes=notes
    )
    
    return Response({
        'id': entry.id,
        'mood_score': entry.mood_score,
        'timestamp': entry.timestamp
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mood_chart(request):
    chart_data = generate_mood_chart(request.user)
    
    if not chart_data:
        return Response({
            'error': 'Not enough data to generate chart'
        }, status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        'chart_image': chart_data
    })