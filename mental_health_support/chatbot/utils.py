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