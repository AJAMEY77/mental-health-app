from django.urls import path
from . import views

urlpatterns = [
    path('log/', views.log_mood, name='mood_dashboard'),
    path('chart/', views.get_mood_chart, name='get_mood_chart'),
   
]