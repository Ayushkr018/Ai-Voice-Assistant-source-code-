from pynput.keyboard import Key, Controller
from time import sleep
import screen_brightness_control as sbc
import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import subprocess

# Initialize the keyboard controller
keyboard = Controller()

# Initialize the speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty("rate", 170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Understanding...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query.lower()

# Volume control functions
def volumeup():
    for i in range(5):
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        sleep(0.1)

def volumedown():
    for i in range(5):
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        sleep(0.1)

def mute():
    keyboard.press(Key.media_volume_mute)
    keyboard.release(Key.media_volume_mute)
    speak("Volume muted")

def unmute():
    keyboard.press(Key.media_volume_mute)
    keyboard.release(Key.media_volume_mute)
    speak("Volume unmuted")

# Brightness control functions
def increase_brightness(value=10):
    current_brightness = sbc.get_brightness(display=0)[0]
    new_brightness = min(current_brightness + value, 100)
    sbc.set_brightness(new_brightness)
    speak(f"Brightness increased to {new_brightness} percent")

def decrease_brightness(value=10):
    current_brightness = sbc.get_brightness(display=0)[0]
    new_brightness = max(current_brightness - value, 0)
    sbc.set_brightness(new_brightness)
    speak(f"Brightness decreased to {new_brightness} percent")

def set_brightness(level=50):
    sbc.set_brightness(level)
    speak(f"Brightness set to {level} percent")

# Media control functions (works with YouTube and media players)
def play_pause():
    keyboard.press(Key.media_play_pause)
    keyboard.release(Key.media_play_pause)
    speak("Media play/pause triggered")

def next_track():
    keyboard.press(Key.media_next)
    keyboard.release(Key.media_next)
    speak("Next track")

def previous_track():
    keyboard.press(Key.media_previous)
    keyboard.release(Key.media_previous)
    speak("Previous track")

# YouTube-specific control
def youtube_control(command):
    # Open YouTube if not already open
    if "youtube.com" not in webbrowser.get().name:
        webbrowser.open("https://www.youtube.com")
    sleep(2)
    
    # Play/pause, next, previous using JS code injection in browser
    if command == "play_pause":
        script = "document.querySelector('video').click();"
    elif command == "next":
        script = "document.querySelector('a[title=Next]').click();"
    elif command == "previous":
        script = "document.querySelector('a[title=Previous]').click();"
    elif command == "mute":
        script = "document.querySelector('video').muted = true;"
    elif command == "unmute":
        script = "document.querySelector('video').muted = false;"
    
    # Execute JavaScript in the browser to control YouTube
    os.system(f"osascript -e 'tell application \"Safari\" to do JavaScript \"{script}\" in document 1'")
    speak(f"YouTube {command.replace('_', ' ')}")

# Main function for voice commands
if __name__ == "__main__":
    while True:
        query = takeCommand()

        if "increase volume" in query:
            volumeup()
            speak("Volume increased")

        elif "decrease volume" in query:
            volumedown()
            speak("Volume decreased")

        elif "mute" in query:
            mute()

        elif "unmute" in query:
            unmute()

        elif "play" in query or "pause" in query:
            play_pause()

        elif "next" in query:
            next_track()

        elif "previous" in query:
            previous_track()

        elif "increase brightness" in query:
            increase_brightness()

        elif "decrease brightness" in query:
            decrease_brightness()

        elif "set brightness" in query:
            speak("What brightness level would you like to set? Say a number between 0 and 100.")
            brightness_level = int(takeCommand())
            set_brightness(brightness_level)

        elif "exit" in query or "goodbye" in query:
            speak("Goodbye, sir!")
            break
