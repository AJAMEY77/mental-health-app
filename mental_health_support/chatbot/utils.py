import openai
from django.conf import settings

# Set OpenAI API Key from settings
#openai.api_key = settings.OPENAI_API_KEY

# chatbot/utils.py (Update get_chatbot_response function)
def get_chatbot_response(user_message, conversation_history=[], system_message=None):
    try:
    # Default system message if none provided
        if system_message is None:
            system_message = "You are a supportive mental health assistant. Provide empathetic responses, coping strategies, and suggest professional help when appropriate. Never diagnose conditions."
        
        # Format conversation history for context
        formatted_history = []
        for entry in conversation_history[-5:]:  # Last 5 conversations for context
            formatted_history.append({"role": "user", "content": entry.user_message})
            formatted_history.append({"role": "assistant", "content": entry.bot_response})
        
        # Add current message
        messages = [
            {"role": "system", "content": system_message},
            *formatted_history,
            {"role": "user", "content": user_message}
        ]
        
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Or your preferred model
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        return "Sorry, I'm experiencing technical difficulties. Please try again later."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


def analyze_message_for_concerns(message):
    """
    Detect potential mental health concerns based on keywords
    """
    # Dictionary of concern types and their keywords
    concern_keywords = {
        'anxiety': ['anxious', 'nervous', 'worry', 'panic', 'fear', 'stress', 'tense'],
        'depression': ['sad', 'depressed', 'hopeless', 'empty', 'worthless', 'tired', 'exhausted'],
        'suicidal': ['suicide', 'kill myself', 'end it all', 'better off dead', 'no reason to live'],
    }
   
    message_lower = message.lower()
    detected_concerns = []
   
    # Check for each concern type
    for concern, keywords in concern_keywords.items():
        for keyword in keywords:
            if keyword in message_lower:
                detected_concerns.append(concern)
                break
   
    # Special handling for suicidal concerns
    if 'suicidal' in detected_concerns:
        return {
            'urgent': True,
            'concerns': detected_concerns,
            'response': "I notice your message contains concerning language. If you're having thoughts of harming yourself, please contact a crisis helpline immediately. The National Suicide Prevention Lifeline is available 24/7 at 1-800-273-8255. Would you like me to provide additional resources?"
        }
   
    elif detected_concerns:
        return {
            'urgent': False,
            'concerns': detected_concerns,
            'response': None  # Let the AI generate a contextual response
        }
   
    return None  # No concerns detected