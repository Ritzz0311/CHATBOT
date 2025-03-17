from flask import Flask, request, jsonify
from chatbot import AdvancedChatbot  # Import your chatbot class

app = Flask(__name__)
chatbot = AdvancedChatbot()  # Initialize your chatbot

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')  # Get user input from the request
    response = chatbot.get_response(user_input)  # Get chatbot's response
    return jsonify({'response': response})  # Return the response as JSON

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the Flask app