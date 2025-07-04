import requests
import pyttsx3
import speech_recognition as sr
import random
import time
import os
from datetime import datetime

# Initialize the speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice
engine.setProperty("rate", 170)  # Speed of speech

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand(retries=3):
    """Takes voice input and retries if not understood. Returns recognized text or 'None'."""
    r = sr.Recognizer()
    for _ in range(retries):
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            r.energy_threshold = 200
            audio = r.listen(source)

        try:
            print("Understanding...")
            query = r.recognize_google(audio, language='en-in')
            print(f"You Said: {query}\n")
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you repeat, please?")
        except sr.RequestError:
            speak("Sorry, there was an issue with the speech recognition service.")
            break
    return "None"

def get_geocode(city):
    api_key = "a1f2e33680d74231b8c728cb8939bf62"  # Replace with your OpenCage API key
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city}&key={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

        if data['results']:
            latitude = data['results'][0]['geometry']['lat']
            longitude = data['results'][0]['geometry']['lng']
            return latitude, longitude
        else:
            return None, "Error: Couldn't fetch geocode data."
    except requests.RequestException as e:
        return None, f"Request error: {e}"

def get_weather_data(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if 'current_weather' in data:
            temperature = data['current_weather']['temperature']
            weather_code = data['current_weather']['weathercode']
            return temperature, weather_code
        else:
            return None, "Error: Couldn't fetch weather data."
    except requests.RequestException as e:
        return None, f"Request error: {e}"

def get_weather_description(weather_code):
    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        61: "Rain showers",
        63: "Moderate rain",
        80: "Rain showers",
        95: "Thunderstorms",
        99: "Severe thunderstorms"
    }
    return descriptions.get(weather_code, "Unknown weather condition")

def get_fun_facts():
    facts = [
        "Did you know? Lightning can strike the same place more than once.",
        "The hottest temperature ever recorded on Earth was 56.7 °C (134 °F) in Death Valley, California.",
        "The coldest temperature ever recorded was -67.7 °C (-89.9 °F) in Antarctica.",
        "A single cloud can weigh over a million pounds!",
        "Rainbows are actually full circles, but we usually only see the top half."
    ]
    return random.choice(facts)

def get_daily_summary(latitude, longitude, update_conversation):
    temperature, weather_code = get_weather_data(latitude, longitude)
    if temperature is not None:
        weather_description = get_weather_description(weather_code)
        summary = f"Today's weather: {temperature}°C with {weather_description}."
        suggestion = ""

        # Suggest actions based on weather description
        if 'rain' in weather_description.lower():
            suggestion = "It looks like it's raining. Don't forget to take an umbrella!"
        elif 'clear' in weather_description.lower():
            suggestion = "It's clear outside. Enjoy your day!"
        elif 'cloud' in weather_description.lower():
            suggestion = "It's cloudy today. You might want to carry a light jacket."
        elif 'snow' in weather_description.lower():
            suggestion = "It's snowing outside. Make sure to dress warmly and stay safe."
        elif 'storm' in weather_description.lower():
            suggestion = "There's a storm coming. Stay indoors and be cautious."

        fact = get_fun_facts()
        full_summary = f"{summary} Here's a fun fact: {fact} {suggestion}"
        update_conversation(full_summary)  # Update GUI conversation
        return full_summary
    else:
        return "Could not get the daily summary."

def set_notification(city, condition, threshold=None):
    with open("weather_notifications.txt", "a") as file:
        if threshold is not None:
            file.write(f"{city},temp,{threshold}\n")
        else:
            file.write(f"{city},weather,{condition}\n")

def check_notifications(update_conversation):
    if not os.path.exists("weather_notifications.txt"):
        return

    with open("weather_notifications.txt", "r") as file:
        notifications = file.readlines()
    
    for line in notifications:
        parts = line.strip().split(',')
        city = parts[0]
        condition_type = parts[1]
        condition_value = parts[2] if len(parts) > 2 else None
        
        latitude, longitude = get_geocode(city)
        temperature, weather_code = get_weather_data(latitude, longitude)
        if temperature is not None:
            weather_description = get_weather_description(weather_code)
            if condition_type == "weather" and condition_value in weather_description:
                speak(f"Alert! The weather in {city} is currently {weather_description}.")
                update_conversation(f"Alert! The weather in {city} is currently {weather_description}.")  # Update GUI conversation
            elif condition_type == "temp" and temperature < float(condition_value):
                speak(f"Alert! The temperature in {city} has dropped below {condition_value}°C.")
                update_conversation(f"Alert! The temperature in {city} has dropped below {condition_value}°C.")  # Update GUI conversation
        time.sleep(60)  # Check every minute

def main(update_conversation):
    speak("Please tell me the name of the city you want to know the current temperature for.")
    update_conversation("Assistant: Please tell me the name of the city you want to know the current temperature for.")
    city = takeCommand()
    if city != "None":
        latitude, longitude = get_geocode(city)
        if latitude is not None and longitude is not None:
            current_temperature, weather_code = get_weather_data(latitude, longitude)
            if current_temperature is not None:
                weather_description = get_weather_description(weather_code)
                response = f"Current temperature in {city} is {current_temperature}°C with {weather_description}."
                speak(response)
                update_conversation(f"Assistant: {response}")  # Update GUI conversation
                
                # Set notification
                speak("Would you like to set a weather notification? Please say yes or no.")
                update_conversation("Assistant: Would you like to set a weather notification? Please say yes or no.")
                response = takeCommand()
                
                if "yes" in response:
                    update_conversation("Assistant: Would you like to set an alert for specific weather conditions or a temperature threshold?")
                    speak("Would you like to set an alert for specific weather conditions or a temperature threshold?")
                    condition_response = takeCommand()
                    if "weather" in condition_response:
                        update_conversation("Assistant: Please say the weather condition you want to be alerted about.")
                        speak("Please say the weather condition you want to be alerted about.")
                        weather_condition = takeCommand()
                        set_notification(city, weather_condition)
                        update_conversation(f"Assistant: Weather notification for {weather_condition} has been set.")
                    elif "temperature" in condition_response:
                        update_conversation("Assistant: Please say the temperature threshold you want to be alerted about.")
                        speak("Please say the temperature threshold you want to be alerted about.")
                        temp_threshold = takeCommand()
                        set_notification(city, None, temp_threshold)
                        update_conversation(f"Assistant: Temperature notification for below {temp_threshold}°C has been set.")
                elif "no" in response:
                    update_conversation("Assistant: Alright, no notification has been set.")
                    speak("Alright, no notification has been set.")
                else:
                    update_conversation("Assistant: Sorry, I didn't catch your response. No notification has been set.")
                    speak("Sorry, I didn't catch your response. No notification has been set.")
                
                # Provide daily summary with suggestions
                daily_summary = get_daily_summary(latitude, longitude, update_conversation)  # Call daily summary function
                speak(daily_summary)
            else:
                update_conversation("Assistant: I couldn’t fetch the current weather.")
                speak("I couldn’t fetch the current weather.")
        else:
            update_conversation("Assistant: I couldn’t get the geocode for that city.")
            speak("I couldn’t get the geocode for that city.")
    else:
        update_conversation("Assistant: I didn’t catch the city name. Please try again.")
        speak("I didn’t catch the city name. Please try again.")

if __name__ == "__main__":
    # Example usage with GUI conversation update
    def update_conversation(text):
        print(text)  # This should be connected to your GUI conversation log

    while True:
        main(update_conversation)
        check_notifications(update_conversation)
