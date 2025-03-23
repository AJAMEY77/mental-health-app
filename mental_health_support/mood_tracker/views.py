from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import MoodEntry
from .utils import analyze_text_sentiment, generate_mood_chart
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required(login_url='/accounts/login/')
def log_mood(request):
    
    if request.method != 'POST':
        return render(request, 'mood_tracker/dashboard.html')
    
    if request.method == 'POST':
        mood_score = None
        notes = ''
        
        if 'mood_score' in request.POST:
            mood_score = int(request.POST.get('mood_score'))
            notes = request.POST.get('notes', '')
        elif 'text' in request.POST:
            text = request.POST.get('text')
            mood_score = analyze_text_sentiment(text)
            notes = text
        else:
            return JsonResponse({'error': 'Either mood_score or text is required'}, status=400)
        
        entry = MoodEntry.objects.create(
            user=request.user,
            mood_score=mood_score,
            notes=notes
        )
        
        return JsonResponse({
            'id': entry.id,
            'mood_score': entry.mood_score,
            'timestamp': entry.timestamp
        })
    
    return render(request, 'dashboard.html')

@login_required
def get_mood_chart(request):
    
    
    chart_data = generate_mood_chart(request.user)
    
    if not chart_data:
        return JsonResponse({'error': 'Not enough data to generate chart'}, status=404)
    
    return JsonResponse({'chart_image': chart_data})
    
