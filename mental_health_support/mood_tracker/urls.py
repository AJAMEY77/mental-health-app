from django.urls import path
from . import views

urlpatterns = [
    path('log/', views.log_mood, name='log_mood'),
    path('chart/', views.get_mood_chart, name='get_mood_chart'),
]