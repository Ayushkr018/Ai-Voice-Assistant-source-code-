import pyttsx3
import datetime
import random

# Initialize the pyttsx3 engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change voice if needed
engine.setProperty("rate", 170)

def speak(audio):
    """Speak the provided text using the pyttsx3 engine."""
    engine.say(audio)
    engine.runAndWait()

def get_day_greeting():
    """Generate a day-specific greeting."""
    day = datetime.datetime.now().strftime("%A")
    day_greetings = [
        f"Happy {day}, hope you're ready to conquer the day!",
        f"Another {day}, another opportunity for greatness!",
        f"It's {day} already! Let's make it productive!",
        f"Good {day} to you! Let’s make today amazing!",
    ]
    return random.choice(day_greetings)

def get_dynamic_mood():
    """Generate a random mood-related message."""
    mood_lines = [
        "The weather's perfect for getting things done today!",
        "I hope you’re feeling as bright as the sun today!",
        "Let’s keep that positive energy going!",
        "I'm here to make your day even better!",
    ]
    return random.choice(mood_lines)

def greetMe(update_conversation):
    """Greet the user based on the time of day and update the conversation."""
    hour = int(datetime.datetime.now().hour)
    day_greeting = get_day_greeting()
    dynamic_mood = get_dynamic_mood()
    
    if hour >= 0 and hour < 12:
        greet_message = f"Good morning, sir! {day_greeting}"
    elif hour >= 12 and hour < 18:
        greet_message = f"Good afternoon, sir! {day_greeting} {dynamic_mood}"
    elif hour >= 18 and hour < 23:
        greet_message = f"Good evening, sir! {day_greeting} How was your day so far?"
    else:
        greet_message = f"Good night, sir! {day_greeting} Don't forget to take it easy tonight."

    speak(greet_message)
    update_conversation(f"Assistant: {greet_message}")  # Log to conversation label

    closing_lines = [
        "How can I make your day even better?",
        "What can I help you with today?",
        "Tell me how I can assist you, I’m ready to help!",
        "Ready when you are, just let me know what you need!"
    ]
    
    closing_message = random.choice(closing_lines)
    speak(closing_message)
    update_conversation(f"Assistant: {closing_message}")  # Log to conversation label
