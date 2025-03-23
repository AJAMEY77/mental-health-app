from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import Conversation
from .utils import analyze_message_for_concerns, get_chatbot_response

@csrf_exempt  # Disable CSRF for API calls (Use proper security in production)
@login_required(login_url="/accounts/login/")
def chat_with_bot(request):
    print(f"Received request method: {request.method}")
    if request.method != 'POST':
        return render(request, 'chatbot/chat.html')
    elif request.method == 'POST':
        print("reequest received")
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            if not user_message:
                return JsonResponse({'error': 'Message is required'}, status=400)
             # Get conversation history
            history = Conversation.objects.filter(user=request.user).order_by('-timestamp')[:5]
            
            # Get chatbot response
            bot_response = get_chatbot_response(user_message, history)
           # bot_response = get_chatbot_response(user_message)
              # Save conversation
            conversation = Conversation.objects.create(
                user=request.user,
                user_message=user_message,
                bot_response=bot_response
            )

            return JsonResponse({
                'response': bot_response,
                'conversation_id': conversation.id
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

            '''
        
            # Analyze message for mental health concerns
            #concern_analysis = analyze_message_for_concerns(user_message)

            # If urgent concern detected, return immediate response
            if concern_analysis and concern_analysis.get('urgent'):
                bot_response = concern_analysis.get('response')

                # Save conversation
                conversation = Conversation.objects.create(
                    user=request.user,
                    user_message=user_message,
                    bot_response=bot_response
                )

                return JsonResponse({
                    'response': bot_response,
                    'conversation_id': conversation.id,
                    'concerns': concern_analysis.get('concerns'),
                    'urgent': True
                })

            # Get conversation history for context
            history = Conversation.objects.filter(user=request.user).order_by('-timestamp')[:5]

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

            if concern_analysis and concern_analysis.get('concerns'):
                response_data['concerns'] = concern_analysis.get('concerns')

            return JsonResponse(response_data)
        '''

        