import pyttsx3
import speech_recognition as sr
import app
from greetMe import greetMe 
import gui  
import pyautogui
import webbrowser
import os
import time
import random
import subprocess
import speedtest
import keyboard
from whatsapp import sendMessage
from game import game_play
from focusgraph import focus_graph
from Translator import translategl
from plyer import notification
from pygame import mixer
from screenrecord import start_screen_recording
import pyjokes
import searchnow
import temperature
import tabs
import turtle
from calculatenumbers import speak, take_command, Calc
import datetime
from Dictapp import openappweb,closeappweb
import calculatenumbers
from NewsRead import latestnews
import voice
from keyboard import ( volume_up, volume_down, mute_volume, unmute_volume, play_pause_media, 
    stop_media, next_track, previous_track, skip_forward_10s, skip_backward_10s, 
    increase_brightness, decrease_brightness, set_brightness_50)
from tabs import open_new_tab, close_tabs
import alarm
from alarm import set_alarm

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Use the Narrator voice (index 1)
engine.setProperty("rate", 170)  # Set speech rate

def speak(audio):
    """Speak function to output text as speech."""
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    """Listen and recognize voice commands."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        try:
            audio = r.listen(source, timeout=8, phrase_time_limit=6)  # Adjusted for better performance
        except sr.WaitTimeoutError:
            return "none"
    try:
        print("Understanding...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
        return query.lower()
    except Exception as e:
        print("Say that again please...")
        return "none"
def get_yes_no_confirmation():
        """Ask for yes/no confirmation via voice and return the result."""
        speak("Are you sure you want to enter focus mode? Please say yes or no.")

def handle_temperature_query(update_conversation):
    temperature.main(update_conversation)

def handle_calculation(query, update_conversation):
    api_key = "2RAXXJ-AP6X66KU7E"  # Replace with your actual API key
    calculatenumbers.Calc(query, api_key, update_conversation)
 
def start_game(update_conversation):
    update_conversation("Assistant: Starting the game section...")
    game_play(update_conversation)

def start_translation(update_conversation):
    update_conversation("Assistant: How can I assist you with translation?")
    speak("How can I assist you with translation?")
    query = takeCommand()  # Assuming you have a way to capture commands
    if query != "None":
        translategl(query, update_conversation)

def activate_alarm_system():
    """Activate alarm system by running the alarm.py file as a subprocess."""
    try:
        # Run the alarm.py file
        speak("Taking you to the alarm system")
        subprocess.run(["python", "alarm.py"])  # Make sure alarm.py is in the same directory or provide full path
        speak("Returning to the main system")
    except Exception as e:
        print(f"Error occurred: {e}")
        speak("Sorry, there was an error accessing the alarm system")
                    
def activate_voice_assistant(update_conversation):
    """Activates the voice assistant and updates conversation in GUI."""
    update_conversation("User: Activating voice assistant...")  # Display in GUI
    speak("I am listening...")
    update_conversation("Assistant: I am listening...")  # Display in GUI
    
    
    last_command = ""
    cooldown_time = 5  # Time to wait before processing next command

    while True:
        query = takeCommand()

        if query == "none":
            continue

        update_conversation(f"You said: {query}")  # Display user's command in GUI

        if "wake up" in query:
            greetMe(update_conversation)  # Call greetMe and update conversation
            response = "I am ready. How can I assist you?"
            speak(response)
            update_conversation(f"Assistant: {response}")  # Show assistant's response

        elif "go to sleep" in query:
            response = "Okay sir, you can call me anytime."
            speak(response)
            update_conversation(f"Assistant: {response}")  # Show assistant's response
            break

        elif "good bye" in query or "quit" in query:
            response = "Goodbye! Have a great day!"
            speak(response)
            update_conversation(f"Assistant: {response}")  # Show assistant's response
            return "close"  # Signal to close GUI

        if "set an alarm" in query:
            activate_alarm_system()
            
        elif "whatsapp" in query:
            sendMessage()
            update_conversation("Assistant: Sending WhatsApp message...")

        elif "tired" in query:
            speak("Playing your favorite songs, sir")
            options = [
                "https://www.youtube.com/watch?v=5gg17XXXiNo",
                "https://www.youtube.com/watch?v=AX6OrbgS8lI",
                "https://www.youtube.com/watch?v=0pWsCiBvLOk&list=RDGMEMQ1dJ7wXfLlqCjwV0xfSNbA&start_radio=1&rv=5gg17XXXiNo"
            ]
            webbrowser.open(random.choice(options))
            update_conversation("Assistant: Playing your favorite music...")

        elif "shutdown the system" in query:
            speak("Are you sure you want to shutdown?")
            speak("Please say 'ok' to confirm or 'no' to cancel.")
            update_conversation("Assistant: Are you sure you want to shutdown?")
    
            confirmation = takeCommand()
            if "ok" in confirmation:
                speak("Shutting down the system.")
                update_conversation("Assistant: Shutting down the system.")
                os.system("shutdown /s /t 1")
            elif "no" in confirmation:
                speak("Shutdown canceled.")
                update_conversation("Assistant: Shutdown canceled.")    
            
            elif "increase volume" in query:
             update_conversation("User: Increasing volume...")
             keyboard.volume_up(update_conversation=update_conversation)

            elif "decrease volume" in query:
             update_conversation("User: Decreasing volume...")
             keyboard.volume_down(update_conversation=update_conversation)

            elif "mute" in query:
              update_conversation("User: Muting volume...")
              keyboard.mute_volume(update_conversation=update_conversation)

            elif "unmute" in query:
              update_conversation("User: Unmuting volume...")
              keyboard.unmute_volume(update_conversation=update_conversation)

            elif "play media" in query or "pause media" in query:
              update_conversation("User: Playing/Pausing media...")
              keyboard.play_pause_media(update_conversation=update_conversation)

            elif "next track" in query:
               update_conversation("User: Skipping to next track...")
               keyboard.next_track(update_conversation=update_conversation)

            elif "previous track" in query:
              update_conversation("User: Playing previous track...")
              keyboard.previous_track(update_conversation=update_conversation)

            elif "stop media" in query:
              update_conversation("User: Stopping media...")
              keyboard.stop_media(update_conversation=update_conversation)

            elif "skip forward" in query:
               update_conversation("User: Skipping forward 10 seconds...")
               keyboard.skip_forward_10s(update_conversation=update_conversation)

            elif "skip backward" in query:
              update_conversation("User: Skipping backward 10 seconds...")
              keyboard.skip_backward_10s(update_conversation=update_conversation)

            elif "increase brightness" in query:
              update_conversation("User: Increasing brightness...")
              keyboard.increase_brightness(update_conversation=update_conversation)

            elif "decrease brightness" in query:
              update_conversation("User: Decreasing brightness...")
              keyboard.decrease_brightness(update_conversation=update_conversation)

            elif "set brightness to 50" in query:
                update_conversation("User: Setting brightness to 50%...")
                keyboard.set_brightness_50(update_conversation=update_conversation)

       
        elif "internet speed" in query:
            wifi = speedtest.Speedtest()
            upload_net = wifi.upload() / 1048576  
            download_net = wifi.download() / 1048576  
            speak(f"Wifi download speed is {download_net:.2f} megabits per second")
            speak(f"Wifi upload speed is {upload_net:.2f} megabits per second")
            update_conversation(f"Assistant: Wifi download speed is {download_net:.2f} Mbps and upload speed is {upload_net:.2f} Mbps.")

        # For opening new tab
        elif "open tab" in query or "new tab" in query:
          speak("Which website do you want to open?")
          website = takeCommand()
          open_new_tab(website, update_conversation)

# For closing tabs
        elif "close tab" in query:
          speak("How many tabs do you want to close?")
          number_of_tabs = takeCommand()
    
          if number_of_tabs.isdigit():
           close_tabs(int(number_of_tabs), update_conversation)
          else:
           speak("Please say a number of tabs to close.")

        elif "open app" in query:
          speak("Which app would you like to open?")
          app_name = takeCommand()
          openappweb(app_name, update_conversation)

        elif "close app" in query:
         speak("Which app would you like to close?")
         app_name = takeCommand()
         closeappweb(app_name, update_conversation)
        
        
        
        elif "google" in query:
          searchnow.searchGoogle(query, update_conversation)
        
        elif "youtube" in query:
           searchnow.searchYoutube(query, update_conversation)
        
        elif "wikipedia" in query:
            searchnow.searchWikipedia(query, update_conversation)
        
        elif "twitter" in query:
          searchnow.searchTwitter(query, update_conversation)
        
        elif "linkedin" in query:
          searchnow.searchLinkedIn(query, update_conversation)

        elif "play a game" in query:
          start_game(update_conversation)

        elif "focus mode" in query:
            speak("Entering focus mode...")
            subprocess.run(["python", r"C:\Users\DELL\OneDrive\Documents\PlatformIO\Projects\AmitAdruino\_pycache_\focusmode.py"])
            update_conversation("Assistant: Focus mode activated.")

        elif "news" in query:
            latestnews(update_conversation)
            
        elif "temperature" in query:  
            handle_temperature_query(update_conversation)
        
        elif "calculate" in query:
          handle_calculation(query, update_conversation)
        
        elif "show my focus" in query:
            update_conversation("Assistant: Showing your focus graph...")
            try:
                focus_graph()  # Call the function to generate the focus graph
                update_conversation("Assistant: Focus graph generated and saved.")
            except Exception as e:
                update_conversation(f"Assistant: Error occurred: {str(e)}")
                print(f"Error generating focus graph: {str(e)}")

        elif "translate" in query:
            query = query.replace("translate", "")
            translategl(query,update_conversation)
            update_conversation(f"Assistant: Translating {query}...")

        elif "schedule my day" in query:
            tasks = []
            speak("Do you want to clear old tasks (Please say 'do it' or 'no need')")
            query = takeCommand().lower()
            if "do it" in query:
                with open("tasks.txt", "w") as file:
                    file.write("")
                no_tasks = int(input("Enter the number of tasks: "))
                for i in range(no_tasks):
                    tasks.append(input("Enter the task: "))
                    with open("tasks.txt", "a") as file:
                        file.write(f"{i+1}. {tasks[i]}\n")
                update_conversation("Assistant: Scheduled your tasks.")
            elif "no need" in query:
                update_conversation("Assistant: Keeping old tasks.")

        elif "show my schedule" in query:
            with open("tasks.txt", "r") as file:
                content = file.read()
            mixer.init()
            mixer.music.load("notification.mp3")
            mixer.music.play()
            notification.notify(
                title="My schedule:",
                message=content,
                timeout=15
            )
            update_conversation("Assistant: Showing your schedule.")

        elif "screenshot" in query:
            im = pyautogui.screenshot()
            im.save("ss.jpg")
            update_conversation("Assistant: Screenshot taken and saved.")

        elif "play the music" in query:
            voice(query)
            update_conversation(f"Assistant:ok sir{query}")

        elif "start screen recording" in query:
            speak("Starting screen recording...")
            start_screen_recording(output_file="screen_recording.mp4", duration=10)
            update_conversation("Assistant: Screen recording started.")

        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)
            update_conversation(f"Assistant: {joke}")

        else:
            speak("Sorry, this type of service is not available.")
            update_conversation("Assistant: Sorry, this type of service is not available.")

        last_command = query  
        time.sleep(cooldown_time)  


if __name__ == "__main__":
    gui.start_gui(activate_voice_assistant) 
    