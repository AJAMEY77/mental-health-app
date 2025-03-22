from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Conversation
from .utils import get_chatbot_response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_with_bot(request):
    user_message = request.data.get('message', '')
   
    if not user_message:
        return Response(
            {'error': 'Message is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
   
    # Get conversation history for context
    history = Conversation.objects.filter(
        user=request.user
    ).order_by('-timestamp')[:5]
   
    # Get response from AI
    bot_response = get_chatbot_response(user_message, history)
   
    # Save the conversation
    conversation = Conversation.objects.create(
        user=request.user,
        user_message=user_message,
        bot_response=bot_response
    )
   
    return Response({
        'response': bot_response,
        'conversation_id': conversation.id
    })




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_with_bot(request):
    user_message = request.data.get('message', '')
   
    if not user_message:
        return Response(
            {'error': 'Message is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
   
    # Get conversation history for context
    history = Conversation.objects.filter(
        user=request.user
    ).order_by('-timestamp')[:5]
   
    # Get response from AI
    bot_response = get_chatbot_response(user_message, history)
   
    # Save the conversation
    conversation = Conversation.objects.create(
        user=request.user,
        user_message=user_message,
        bot_response=bot_response
    )
   
    return Response({
        'response': bot_response,
        'conversation_id': conversation.id
    })

