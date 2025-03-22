from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Conversation
from .utils import analyze_message_for_concerns, get_chatbot_response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_with_bot(request):
    user_message = request.data.get('message', '')
    
    if not user_message:
        return Response(
            {'error': 'Message is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Analyze message for mental health concerns
    concern_analysis = analyze_message_for_concerns(user_message)
    
    # If urgent concern detected, return immediate response
    if concern_analysis and concern_analysis.get('urgent'):
        bot_response = concern_analysis.get('response')
        
        # Save conversation
        conversation = Conversation.objects.create(
            user=request.user,
            user_message=user_message,
            bot_response=bot_response
        )
        
        return Response({
            'response': bot_response,
            'conversation_id': conversation.id,
            'concerns': concern_analysis.get('concerns'),
            'urgent': True
        })
    
    # Get conversation history for context
    history = Conversation.objects.filter(
        user=request.user
    ).order_by('-timestamp')[:5]
    
    # Enhance prompt with detected concerns
    system_message = "You are a supportive mental health assistant. Provide empathetic responses, coping strategies, and suggest professional help when appropriate. Never diagnose conditions."
    
    if concern_analysis and concern_analysis.get('concerns'):
        concerns_list = ", ".join(concern_analysis.get('concerns'))
        system_message += f" The user's message contains language related to {concerns_list}. Be particularly supportive and provide relevant coping strategies."
    
    # Get response from AI
    bot_response = get_chatbot_response(user_message, history, system_message)
    
    # Save the conversation
    conversation = Conversation.objects.create(
        user=request.user,
        user_message=user_message,
        bot_response=bot_response
    )
    
    response_data = {
        'response': bot_response,
        'conversation_id': conversation.id
    }
    
    # Include concerns in response if detected
    if concern_analysis and concern_analysis.get('concerns'):
        response_data['concerns'] = concern_analysis.get('concerns')
    
    return Response(response_data)