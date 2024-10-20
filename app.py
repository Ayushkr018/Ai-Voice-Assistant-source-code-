import os
import webbrowser
import psutil
import subprocess
import pyttsx3

# Initialize speech engine for responses
engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Optional: set to a specific voice
engine.setProperty("rate", 170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to open an application
def open_app(app_name):
    try:
        if app_name.lower() == "notepad":
            os.system("notepad")
            speak("Opening Notepad")
        elif app_name.lower() == "calculator":
            os.system("calc")
            speak("Opening Calculator")
        elif app_name.lower() == "spotify":
            webbrowser.open("https://www.spotify.com")
            speak("Opening Spotify")
        elif app_name.lower() == "chrome":
            os.system("start chrome")
            speak("Opening Google Chrome")
        else:
            # Fallback: Try using the app name directly
            subprocess.Popen(app_name)
            speak(f"Trying to open {app_name}")
    except Exception as e:
        speak(f"Sorry, I couldn't open {app_name}.")
        print(f"Error opening {app_name}: {e}")

# Function to close an application
def close_app(app_name):
    try:
        found = False
        for process in psutil.process_iter(['pid', 'name']):
            # Search for partial matches in the process name
            if app_name.lower() in process.info['name'].lower():
                print(f"Found process: {process.info}")  # Debug print
                os.system(f"taskkill /f /pid {process.info['pid']}")
                speak(f"Closing {app_name}")
                found = True
                break
        if not found:
            speak(f"{app_name} is not running.")
    except Exception as e:
        print(f"Error occurred: {e}")
        speak(f"Sorry, I couldn't close {app_name}. Please try again.")