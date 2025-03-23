from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.get_resources, name='resources'),
    path('self-help/', views.get_self_help_exercises, name='get_self_help_exercises'),
    path('recommendations/', views.get_recommendations, name='get_recommendations'),

]