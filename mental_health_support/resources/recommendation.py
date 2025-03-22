from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Resource, SelfHelpExercise

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_resources(request):
    category = request.query_params.get('category', None)
    
    if category:
        resources = Resource.objects.filter(category=category)
    else:
        resources = Resource.objects.all()
    
    return Response([{
        'id': r.id,
        'title': r.title,
        'description': r.description,
        'url': r.url,
        'category': r.category
    } for r in resources])

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_self_help_exercises(request):
    category = request.query_params.get('category', None)
    
    if category:
        exercises = SelfHelpExercise.objects.filter(category=category)
    else:
        exercises = SelfHelpExercise.objects.all()
    
    return Response([{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'instructions': e.instructions,
        'category': e.category
    } for e in exercises])