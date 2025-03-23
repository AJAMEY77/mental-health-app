from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Resource, SelfHelpExercise
from .recommendation import get_personalized_recommendations

def home(request):
    """Render the home page."""
    return render(request, 'base.html')

@login_required(login_url='/accounts/login/')
def get_resources(request):
    """Render resources page with optional category filter."""
    category = request.GET.get('category', None)
    
    if category:
        resources = Resource.objects.filter(category=category)
    else:
        resources = Resource.objects.all()
    
    context = {
        'resources': resources
    }
    
    return render(request, 'resources/index.html', context)

@login_required(login_url='/accounts/login/')
def get_self_help_exercises(request):
    """Render self-help exercises page with optional category filter."""
    category = request.GET.get('category', None)
    
    if category:
        exercises = SelfHelpExercise.objects.filter(category=category)
    else:
        exercises = SelfHelpExercise.objects.all()
    
    context = {
        'exercises': exercises
    }
    
    return render(request, 'self_help_exercises.html', context)

@login_required(login_url='/accounts/login/')
def get_recommendations(request):
    """Render recommendations based on user preferences."""
    recommendation = get_personalized_recommendations(request.user)
    
    context = {
        'resources': recommendation['resources'],
        'exercises': recommendation['exercises'],
        'top_categories': recommendation['top_categories']
    }
    
    return render(request, 'recommendations.html', context)
