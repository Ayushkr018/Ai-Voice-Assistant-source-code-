import requests
import pyttsx3
import speech_recognition as sr

# Initialize the speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change index to the desired voice ID
engine.setProperty("rate", 170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 400
        audio = r.listen(source)

    try:
        print("Understanding...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except sr.UnknownValueError:
        print("Sorry, I did not understand the audio.")
        return "None"
    except sr.RequestError:
        print("Sorry, there was an issue with the speech recognition service.")
        return "None"
    return query.lower()

def get_temperature(city):
    # Your OpenWeatherMap API key
    api_key = "YOUR__API_KEY"
    # Endpoint for the current weather
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    # Make the request to the API
    try:
        response = requests.get(url)
        data = response.json()
        
        # Check if the request was successful
        if response.status_code == 200:
            # Extract the temperature and weather description from the data
            temperature = data['main']['temp']
            weather_description = data['weather'][0]['description']
            
            # Suggest actions based on the weather conditions
            suggestion = ""
            if 'rain' in weather_description:
                suggestion = "It looks like it's raining. Don't forget to take an umbrella!"
            elif 'clear' in weather_description:
                suggestion = "It's clear outside. Enjoy your day!"
            elif 'cloud' in weather_description:
                suggestion = "It's cloudy today. You might want to carry a light jacket."
            elif 'snow' in weather_description:
                suggestion = "It's snowing outside. Make sure to dress warmly and stay safe."
            elif 'storm' in weather_description:
                suggestion = "There's a storm coming. Stay indoors and be cautious."
            else:
                suggestion = "Check the weather before heading out."

            return f"Current temperature in {city} is {temperature}°C. {suggestion}"
        else:
            return f"Error: {data.get('message', 'Sorry, I couldn’t fetch the temperature.')}"
    except requests.RequestException as e:
        return f"Request error: {e}"

def get_temperatures_for_country(country):
    # List of cities in the country (for demonstration purposes, this is a small sample)
    # You can extend this list or fetch it from an external source
    cities = ["London", "Manchester", "Birmingham", "Leeds", "Glasgow"]
    temperatures = []

    for city in cities:
        temp_info = get_temperature(city)
        temperatures.append(temp_info)
    
    return "\n".join(temperatures)

def main():
    speak("Please tell me the name of the country you want to know the temperatures for.")
    country = takeCommand()
    if country != "None":
        # Fetch and speak temperature information for all cities in the country
        temperature_summary = get_temperatures_for_country(country)
        speak(temperature_summary)
    else:
        speak("I didn’t catch the country name. Please try again.")

if __name__ == "__main__":
    main()
