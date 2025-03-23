import google.generativeai as genai

# Your API key
API_KEY = 'AIzaSyD_eLdW38a5g17DsSbJ-otqzI0GciK9DNA'

def test_gemini_api():
    try:
        # Configure the API
        genai.configure(api_key=API_KEY)
        
        # List available models
        print("\nListing available models:")
        models = genai.list_models()
        for m in models:
            print(f"\nModel: {m.name}")
            print(f"Description: {m.description}")
            print(f"Generation Methods: {m.supported_generation_methods}")
            print("-" * 50)
        
        # Try to generate content
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hello, how are you?")
        print("\nTest response:", response.text)
        
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    test_gemini_api()