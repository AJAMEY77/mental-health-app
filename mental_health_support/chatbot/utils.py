import google.generativeai as genai
from django.conf import settings

def get_chatbot_response(user_message, conversation_history=[], system_message=None):
    try:
        # Configure API key
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        # Create the model
        model = genai.GenerativeModel('models/gemini-2.0-flash-001')
        
        # Default system message if none provided
        if system_message is None:
            system_message = (
                "You are a supportive mental health assistant. Provide empathetic responses, "
                "coping strategies, and suggest professional help when appropriate. Never diagnose conditions."
            )
        
        # Format conversation history for context
        formatted_history = []
        history_to_use = conversation_history[:5]  # Take last 5 conversations
        
        for entry in history_to_use:
            formatted_history.append(f"User: {entry.user_message}")
            formatted_history.append(f"Assistant: {entry.bot_response}")
        
        # Construct prompt with context
        prompt = f"""
        {system_message}
        
        Previous conversation:
        {chr(10).join(formatted_history) if formatted_history else 'No previous conversation'}
        
        Current conversation:
        User: {user_message}
        Assistant:"""
        
        # Generate response
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text.strip()
        return "I apologize, but I couldn't generate a response. Please try again."
        
    except Exception as e:
        print(f"Error in get_chatbot_response: {str(e)}")
        return f"I encountered an error: {str(e)}"

def analyze_message_for_concerns(message):
    """
    Analyze message for potential mental health concerns
    Returns dictionary with urgent flag and detected concerns
    """
    try:
        # Configure API key
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        # Create model for analysis
        model = genai.GenerativeModel('models/gemini-2.0-flash-001')
        
        # Analysis prompt
        analysis_prompt = f"""
        Analyze this message for mental health concerns. Look for:
        1. Signs of crisis or emergency
        2. Mental health symptoms
        3. Level of distress
        
        Message: {message}
        
        Respond in JSON format:
        {{
            "urgent": true/false,
            "concerns": ["concern1", "concern2"],
            "severity": "low/medium/high"
        }}
        """
        
        # Get analysis
        response = model.generate_content(analysis_prompt)
        
        if response and response.text:
            analysis = response.text.strip()
            
            # If urgent concerns detected
            if '"urgent": true' in analysis.lower():
                return {
                    'urgent': True,
                    'concerns': ['crisis'],
                    'response': (
                        "I notice some concerning thoughts in your message. "
                        "If you're having thoughts of self-harm or feeling unsafe, "
                        "please reach out to emergency services or call the National "
                        "Suicide Prevention Lifeline at 1-800-273-8255. They are "
                        "available 24/7 to help."
                    )
                }
            
            return {
                'urgent': False,
                'concerns': ['general'],
                'response': None
            }
            
    except Exception as e:
        print(f"Error in analyze_message_for_concerns: {str(e)}")
        return None

    return None