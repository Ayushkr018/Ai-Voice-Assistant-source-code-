import time
import pyttsx3
from datetime import datetime, timedelta
from playsound import playsound
import threading
import speech_recognition as sr

# Initialize text-to-speech engine
engine = pyttsx3.init("sapi5")
engine.setProperty("rate", 160)

def speak(audio, update_conversation=None):
    """Speak the given audio and update the conversation."""
    engine.say(audio)
    engine.runAndWait()
    if update_conversation:
        update_conversation(f"Assistant: {audio}")

def listen(update_conversation=None):
    """Listen for voice input and update the conversation."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower().strip()
            print(f"You said: {command}")
            if update_conversation:
                update_conversation(f"User: {command}")
            return command
        except sr.UnknownValueError:
            error_msg = "Sorry, I didn't catch that. Please try again."
            speak(error_msg, update_conversation)
            return None
        except sr.RequestError:
            error_msg = "Sorry, there seems to be a problem with the speech recognition service."
            speak(error_msg, update_conversation)
            return None

def log_to_file(message):
    """Log the current status to a text file."""
    with open("AlarmText.txt", "a") as log_file:
        log_file.write(f"{message}\n")

def play_music(stop_event, update_conversation=None):
    """Play the alarm music in a loop until stopped."""
    music_file = "music.mp3"  # Add your own alarm music file here
    while not stop_event.is_set():
        playsound(music_file)
    if update_conversation:
        update_conversation("Assistant: Music stopped.")

def set_alarm(alarm_time, update_conversation=None):
    """Set the alarm and handle stop/snooze."""
    try:
        alarm_time_obj = datetime.strptime(alarm_time, "%H:%M")  # Convert alarm time string to datetime object
    except ValueError:
        error_msg = "Invalid time format. Please use HH:MM format."
        speak(error_msg, update_conversation)
        return

    stop_event = threading.Event()  # Event to stop the music thread
    while True:
        current_time = datetime.now().strftime("%H:%M")
        log_to_file(f"Current time: {current_time}, Alarm time: {alarm_time}")
        if update_conversation:
            update_conversation(f"Assistant: Current time: {current_time}, Alarm time: {alarm_time}")

        if current_time == alarm_time:
            speak("Alarm ringing!", update_conversation)
            log_to_file("Alarm ringing!")
            music_thread = threading.Thread(target=play_music, args=(stop_event, update_conversation))
            music_thread.start()  # Start playing the music in a separate thread
            
            while True:
                speak("Do you want to stop or snooze the alarm? Say stop or snooze.", update_conversation)
                response = listen(update_conversation)
                if response == "stop":
                    stop_event.set()  # Signal the music thread to stop
                    music_thread.join()  # Wait for the music thread to finish
                    speak("Alarm stopped.", update_conversation)
                    log_to_file("Alarm stopped.")
                    return
                elif response == "snooze":
                    stop_event.set()  # Signal the music thread to stop
                    music_thread.join()  # Wait for the music thread to finish
                    snooze_time = 5  # Snooze for 5 minutes
                    new_alarm_time = (datetime.now() + timedelta(minutes=snooze_time)).strftime("%H:%M")
                    speak(f"Snoozing for {snooze_time} minutes.", update_conversation)
                    log_to_file(f"Snoozing for {snooze_time} minutes.")
                    time.sleep(snooze_time * 60)  # Wait for snooze duration
                    alarm_time = new_alarm_time  # Update alarm time to the new snooze time
                    break
                else:
                    speak("Invalid response, please say stop or snooze.", update_conversation)

        time.sleep(1)  # Check the time every second

def add_study_routine(routine, update_conversation=None):
    """Add a new study routine to the file."""
    with open("study_routines.txt", "a") as file:
        file.write(routine + "\n")
    speak("Study routine added.", update_conversation)

def load_study_routines(update_conversation=None):
    """Load and display study routines."""
    try:
        with open("study_routines.txt", "r") as file:
            routines = file.readlines()
        if routines:
            speak("Your Study Routines are:", update_conversation)
            for idx, routine in enumerate(routines, start=1):
                speak(f"{idx}. {routine.strip()}", update_conversation)
        else:
            speak("No study routines found.", update_conversation)
    except FileNotFoundError:
        speak("No study routines found.", update_conversation)

def main(update_conversation=None):
    """Main function to interact with the user."""
    while True:
        speak("Welcome to the alarm system. Choose an option: Set alarm, Add study routine, Show study routines, or Exit.", update_conversation)
        choice = listen(update_conversation)

        if choice in ["set alarm", "add alarm", "alarm"]:
            speak("Please say the alarm time in HH:MM format.", update_conversation)
            alarm_time = listen(update_conversation)  # Listening for the alarm time
            if alarm_time:
                set_alarm(alarm_time, update_conversation)
        
        elif choice in ["add study routine", "study routine", "routine"]:
            speak("Please say your study routine.", update_conversation)
            routine = listen(update_conversation)
            if routine:
                add_study_routine(routine, update_conversation)

        elif choice in ["show study routines", "show routines", "show timing", "timing"]:
            load_study_routines(update_conversation)

        elif choice in ["exit", "quit", "stop"]:
            speak("Exiting the alarm system.", update_conversation)
            break

        else:
            speak("Sorry, I didn't understand that. Please try again.", update_conversation)

if __name__ == "__main__":
    main()
