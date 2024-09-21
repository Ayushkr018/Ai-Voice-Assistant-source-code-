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
    api_key = "e5a46f38e4dd454da6d486d8c0218195"  # Replace with your OpenCage API key
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

def get_daily_summary(latitude, longitude):
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
        return f"{summary} Here's a fun fact: {fact} {suggestion}"
    else:
        return "Could not get the daily summary."

def set_notification(city, condition, threshold=None):
    with open("weather_notifications.txt", "a") as file:
        if threshold is not None:
            file.write(f"{city},temp,{threshold}\n")
        else:
            file.write(f"{city},weather,{condition}\n")

def check_notifications():
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
            elif condition_type == "temp" and temperature < float(condition_value):
                speak(f"Alert! The temperature in {city} has dropped below {condition_value}°C.")
        time.sleep(60)  # Check every minute

def main():
    speak("Please tell me the name of the city you want to know the current temperature for.")
    city = takeCommand()
    if city != "None":
        latitude, longitude = get_geocode(city)
        if latitude is not None and longitude is not None:
            current_temperature, weather_code = get_weather_data(latitude, longitude)
            if current_temperature is not None:
                weather_description = get_weather_description(weather_code)
                speak(f"Current temperature in {city} is {current_temperature}°C with {weather_description}.")
                
                # Set notification
                speak("Would you like to set a weather notification? Please say yas or no.")
                response = takeCommand()
                
                if "yas" in response or "ok" in response:
                    speak("Would you like to set an alert for specific weather conditions or a temperature threshold?")
                    condition_response = takeCommand()
                    if "weather" in condition_response:
                        speak("Please say the weather condition you want to be alerted about.")
                        weather_condition = takeCommand()
                        set_notification(city, weather_condition)
                        speak(f"Weather notification for {weather_condition} has been set.")
                    elif "temperature" in condition_response:
                        speak("Please say the temperature threshold you want to be alerted about.")
                        temp_threshold = takeCommand()
                        set_notification(city, None, temp_threshold)
                        speak(f"Temperature notification for below {temp_threshold}°C has been set.")
                elif "no" in response:
                    speak("Alright, no notification has been set.")
                else:
                    speak("Sorry, I didn't catch your response. No notification has been set.")
                
                # Provide daily summary with suggestions
                daily_summary = get_daily_summary(latitude, longitude)
                speak(daily_summary)
            else:
                speak("I couldn’t fetch the current weather.")
        else:
            speak("I couldn’t get the geocode for that city.")
    else:
        speak("I didn’t catch the city name. Please try again.")

if __name__ == "__main__":
    while True:
        main()
        check_notifications()
