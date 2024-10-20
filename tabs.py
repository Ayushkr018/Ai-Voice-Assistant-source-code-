import pyautogui
import pyttsx3
from time import sleep
import webbrowser

# Initialize the speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 200)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to open a new tab in the browser
def open_new_tab(url, update_conversation):
    try:
        speak("Opening a new tab")
        update_conversation("Assistant: Opening a new tab")
        webbrowser.open_new_tab(url)
        update_conversation(f"Assistant: Opened {url} in a new tab")
    except Exception as e:
        speak(f"Sorry, I couldn't open the tab.")
        update_conversation(f"Assistant: Failed to open the tab - {str(e)}")

# Function to close a certain number of tabs in the browser
def close_tabs(tab_count, update_conversation):
    speak(f"Closing {tab_count} tabs.")
    update_conversation(f"Assistant: Closing {tab_count} tabs")
    
    for _ in range(tab_count):
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)  # Small delay between closing tabs
    speak(f"{tab_count} tabs closed.")
    update_conversation(f"Assistant: {tab_count} tabs closed.")
