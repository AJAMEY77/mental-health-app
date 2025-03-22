import openai
from django.conf import settings

# Set OpenAI API Key from settings
#openai.api_key = settings.OPENAI_API_KEY

def get_chatbot_response(user_message, conversation_history=[]):
    try:
        # Format conversation history (keeping last 5 exchanges for context)
        formatted_history = []
        for entry in conversation_history[-5:]:  
            formatted_history.append({"role": "user", "content": entry.get("user_message", "")})
            formatted_history.append({"role": "assistant", "content": entry.get("bot_response", "")})

        # Add system prompt and user message
        messages = [
            {"role": "system", "content": (
                "You are a supportive mental health assistant. "
                "Provide empathetic responses, coping strategies, "
                "and suggest professional help when appropriate. "
                "Never diagnose conditions."
            )},
            *formatted_history,
            {"role": "user", "content": user_message[:500]}  # Limit input length
        ]

        # Generate response from OpenAI API
        response = openai.ChatCompletion.create(
            model=settings.OPENAI_MODEL,  # Fetch model dynamically from settings
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )

        return response.choices[0].message["content"]

    except openai.error.OpenAIError as e:
        return "Sorry, I'm experiencing technical difficulties. Please try again later."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
    # chatbot/utils.py (Add to existing file)
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