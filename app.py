from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyC5BE0bAVJQxdCSqtdPLeKaudN7rG7XG9o"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_emotional_support(user_input):
    prompt = f"""You are a compassionate mental health support assistant. The user has shared: "{user_input}"

    Please respond with:
    1. Empathetic acknowledgment of their feelings
    2. Gentle exploration of their emotions
    3. Validation of their experience
    4. A supportive question to help them express more

    Keep the response warm, understanding, and conversational. Don't jump to solutions yet - focus on emotional support first."""
    
    response = model.generate_content(prompt)
    return response.text

def get_lifestyle_recommendation(user_input, conversation_history):
    prompt = f"""Based on the following conversation about the user's mental health state, provide specific lifestyle recommendations for nutrition and activities. 
    Consider their emotional state and provide gentle, practical advice that can help improve their well-being.
    
    Conversation History:
    {conversation_history}
    
    User's Current State: {user_input}
    
    Please provide recommendations in a structured format with:
    1. A brief acknowledgment of their feelings
    2. Specific nutrition suggestions
    3. Activity recommendations
    4. A supportive closing message
    
    Keep the tone warm and encouraging."""
    
    response = model.generate_content(prompt)
    return response.text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    conversation_history = request.json.get('history', [])
    
    if not user_input:
        return jsonify({'response': 'Please provide a message.'})
    
    try:
        # First, provide emotional support
        if len(conversation_history) < 2:  # If it's early in the conversation
            response = get_emotional_support(user_input)
        else:  # After some conversation, provide recommendations
            response = get_lifestyle_recommendation(user_input, conversation_history)
        
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True) 