from flask import Flask, request, jsonify
import speech_recognition as sr
import pyttsx3
import re
import requests
from datetime import datetime

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# NewsAPI configuration
NEWS_API_KEY = "8fa11862-e86b-484c-98fd-4dbce9b7d8dd"  # Replace with your NewsAPI key
NEWS_API_URL = "https://content.guardianapis.com/search"

app = Flask(__name__)

class AdvancedChatbot:
    def __init__(self):
        # Predefined rules and responses
        self.responses = {
            r"hello|hi|hey": "Hello! How can I help you?",
            r"how are you|how's it going|how do you do": "I'm just a bot, but I'm doing great! How about you?",
            r"what's your name|who are you": "I'm an advanced chatbot. You can call me ChatBot!",
            r"tell me a joke|say something funny|joke": self.get_joke,  # Dynamic response from an API
            r"weather in (.+)": self.get_weather,  # Dynamic response for weather
            r"what's the time|tell me the time|what time is it|time": self.get_time,  # Dynamic response for time
            r"what's the date|tell me the date|what date is it|date": self.get_date,  # Dynamic response for date
            r"news|latest news|top headlines": self.get_news,  # Dynamic response for news
            r"bye|goodbye": "Goodbye! Have a great day!",
            "default": "I'm sorry, I don't understand that. Can you please rephrase?"
        }

    def get_response(self, user_input):
        """
        Matches user input with predefined rules and returns a response.
        """
        user_input = user_input.lower()  # Convert input to lowercase for case-insensitive matching
        for pattern, response in self.responses.items():
            if re.search(pattern, user_input):  # Check if the input matches the pattern
                if callable(response):  # If the response is a function, call it
                    return response(user_input)
                return response
        return self.responses["default"]  # Return default response if no match is found

    def get_joke(self, user_input):
        """
        Fetches a random joke from an API.
        """
        try:
            response = requests.get("https://official-joke-api.appspot.com/random_joke")
            joke = response.json()
            return f"{joke['setup']} {joke['punchline']}"
        except:
            return "Sorry, I couldn't fetch a joke right now."

    def get_weather(self, user_input):
        """
        Fetches the weather for a specific city from an API.
        """
        city = re.search(r"weather in (.+)", user_input).group(1) if isinstance(user_input, str) else user_input
        try:
            api_key = "your_openweathermap_api_key"  # Replace with your OpenWeatherMap API key
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            if data["cod"] == 200:
                weather = data["weather"][0]["description"]
                temp = data["main"]["temp"]
                return f"The weather in {city} is {weather} with a temperature of {temp}°C."
            else:
                return f"Sorry, I couldn't find the weather for {city}."
        except:
            return "Sorry, there was an issue fetching the weather."

    def get_time(self, user_input):
        """
        Returns the current time.
        """
        now = datetime.now()
        return f"The current time is {now.strftime('%H:%M:%S')}."

    def get_date(self, user_input):
        """
        Returns the current date.
        """
        now = datetime.now()
        return f"Today's date is {now.strftime('%A, %B %d, %Y')}."

    def get_news(self, user_input):
        """
        Fetches the latest news headlines using NewsAPI.
        """
        try:
            params = {
                "apiKey": NEWS_API_KEY,
                "q": "technology",
                "pageSize": 5  # Limit to 5 headlines
            }
            response = requests.get(NEWS_API_URL, params=params)
            data = response.json()
            if data["status"] == "ok":
                articles = data["articles"]
                if articles:  # Check if articles list is not empty
                    headlines = [article["title"] for article in articles]
                    return "Here are the latest news headlines: " + ". ".join(headlines)
                else:
                    return "Sorry, no news articles were found."
            else:
                return "Sorry, I couldn't fetch the news right now."
        except Exception as e:
            return "Sorry, there was an issue fetching the news."

# Initialize the chatbot
chatbot = AdvancedChatbot()

@app.route('/chat', methods=['POST'])
def chat():
    """
    API endpoint to interact with the chatbot.
    """
    user_input = request.json.get('message')
    response = chatbot.get_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)