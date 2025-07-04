import pyautogui
import pyttsx3
import webbrowser
from time import sleep
import pygetwindow as gw
import re

# Initialize speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Zira
engine.setProperty("rate", 200)

# Speak function
def speak(audio):
    print(f"Assistant: {audio}")
    engine.say(audio)
    engine.runAndWait()

# Fallback update_conversation if not provided
def default_update_conversation(text):
    print(text)

# Focus the Brave browser window
def focus_brave_window():
    try:
        brave_windows = [w for w in gw.getWindowsWithTitle('Brave')]
        if brave_windows:
            brave_windows[0].activate()
            sleep(0.5)
            return True
    except Exception as e:
        print("Error focusing Brave:", e)
    return False


# Open a new tab in Brave
def open_new_tab(url, update_conversation=default_update_conversation):
    try:
        speak("Opening a new tab")
        update_conversation("Assistant: Opening a new tab")
        webbrowser.get(using='windows-default').open_new_tab(url)
        update_conversation(f"Assistant: Opened {url} in a new tab")
    except Exception as e:
        speak("Sorry, I couldn't open the tab.")
        update_conversation(f"Assistant: Failed to open the tab - {str(e)}")

# Extract a number from spoken or written input
def extract_number_from_text(text):
    number_words = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
    }

    text = text.lower()

    # Match numeric digits
    digit_match = re.search(r'\d+', text)
    if digit_match:
        return int(digit_match.group())

    # Match number words
    for word in number_words:
        if word in text:
            return number_words[word]

    return None

# Close tabs in Brave
def close_tabs(tab_count, update_conversation=default_update_conversation):
    if not focus_brave_window():
        speak("Brave browser is not open or not detected.")
        update_conversation("Assistant: Could not focus on Brave browser.")
        return

    speak(f"Closing {tab_count} tab(s).")
    update_conversation(f"Assistant: Closing {tab_count} tab(s)")

    for _ in range(tab_count):
        pyautogui.hotkey("ctrl", "w")
        sleep(0.4)

    speak(f"{tab_count} tab(s) closed.")
    update_conversation(f"Assistant: {tab_count} tab(s) closed.")
