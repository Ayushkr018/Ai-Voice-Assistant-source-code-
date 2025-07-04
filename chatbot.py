# Import necessary libraries
import pyttsx3
import speech_recognition as sr
import random
import datetime

from keyboard import update_conversation

# Initialize text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Choose a voice (1 for female)

def speak(audio):
    """Converts text to speech."""
    engine.say(audio)
    engine.runAndWait()

def listen():
    """Listens for voice input and returns it as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-IN')
        print(f"You said: {query}")
        return query.lower()
    except Exception as e:
        print("Sorry, I didn't catch that. Please try again.")
        return None

def get_time():
    """Return the current time."""
    now = datetime.datetime.now()
    return now.strftime("%H:%M")

def chatbot_response(user_input, context, update_conversation):
    """Generate a response based on user input and context."""
    responses = {
        "hello": ["Hi there!", "Hello! How can I brighten your day?", "Hey! What can I do for you today?"],
        "how are you": ["I'm just a program, but thanks for asking! How about you?", "Doing great! What's new with you?"],
        "what's your name": ["I'm Ellyse, your virtual assistant. Nice to meet you!", "You can call me Ellyse!"],
        "tell me a joke": ["Why did the scarecrow win an award? Because he was outstanding in his field!", "I told my computer I needed a break, and now it won't stop sending me beach wallpapers!"],
        "i need help": ["I'm here for you! What do you need assistance with?", "Sure! Just let me know how I can help you."],
        "what's the time": [f"The current time is {get_time()}.", f"Right now, it is {get_time()}."],
        "goodbye": ["Goodbye! Have a fantastic day!", "See you later! Don't hesitate to chat again!"],
        "what do you like": ["I love learning new things and chatting with you!", "Talking with you is my favorite pastime!"]
    }
    
    # Follow-up conversation based on previous context
    if context.get("asking_name"):
        context["asking_name"] = False
        return "What about you? What's your name?"
    
    if context.get("user_name"):
        if "how are you" in user_input:
            return f"I'm doing well, {context['user_name']}! How about you? "
    
    if "my name is" in user_input:
        name = user_input.split("my name is ")[-1].strip()
        context["user_name"] = name
        return f"Nice to meet you, {name}!"

    # Default response if input is not recognized
    default_response = "I'm sorry, I don't understand. Can you please rephrase?"

    # Check if the user input is in the predefined responses
    for key in responses:
        if key in user_input:
            if key == "what's your name":
                context["asking_name"] = True
            response = random.choice(responses[key])
            update_conversation(f"Assistant: {response}")  # Update the conversation
            return response
    
    # Fun and interesting topics
    if "tell me something interesting" in user_input:
        interesting_facts = [
            "Did you know honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3000 years old and still edible!",
            "Octopuses have three hearts and blue blood!",
            "Bananas are berries, but strawberries aren't!"
        ]
        response = random.choice(interesting_facts)
        update_conversation(f"Assistant: {response}")  # Update the conversation
        return response

    update_conversation(f"Assistant: {default_response}")  # Update the conversation
    return default_response

if __name__ == "__main__":
    speak("Hello! I am your Ellyse. How can I assist you today?")
    
    context = {}
    
    while True:
        user_input = listen()
        if user_input:
            response = chatbot_response(user_input, context, update_conversation)  # Pass update_conversation function
            speak(response)
            if "goodbye" in user_input:
                break
