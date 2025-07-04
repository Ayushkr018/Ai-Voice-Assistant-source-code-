import pyttsx3
import speech_recognition as sr
import time
import pyautogui
import subprocess
import os

# Text-to-Speech engine setup
engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice
engine.setProperty("rate", 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    """Takes voice input from the user and returns as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 200
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
    except Exception:
        print("Didn't catch that. Try again.")
        return "none"
    return query.lower()

def send_gmail(update_conversation):
    speak("Opening Gmail to compose a new email.")
    update_conversation("Assistant: Opening Gmail in Brave browser.")

    # Path to Brave browser executable
    brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
    gmail_url = "https://mail.google.com/mail/u/0/#inbox?compose=new"

    try:
        subprocess.Popen([brave_path, gmail_url])
        time.sleep(10)  # Wait for Gmail to load completely
    except Exception as e:
        speak("Could not open Gmail.")
        update_conversation("Assistant: Failed to open Gmail.")
        print("Error:", e)
        return

    # Click inside Gmail to focus
    pyautogui.click(400, 400)
    time.sleep(2)

    # Recipient
    speak("Who do you want to send the email to?")
    update_conversation("Assistant: Waiting for recipient email...")
    to = takeCommand()
    update_conversation(f"User: {to}")
    if to == "none":
        speak("Sorry, I couldn't understand the recipient.")
        return
    pyautogui.write(to)
    pyautogui.press("tab")  # Move to subject
    time.sleep(1)

    # Subject
    speak("What is the subject?")
    update_conversation("Assistant: Waiting for subject...")
    subject = takeCommand()
    update_conversation(f"User: {subject}")
    if subject == "none":
        speak("Sorry, I couldn't understand the subject.")
        return
    pyautogui.write(subject)
    pyautogui.press("tab")  # Move to body
    time.sleep(1)

    # Message
    speak("What message do you want to send?")
    update_conversation("Assistant: Waiting for message...")
    message = takeCommand()
    update_conversation(f"User: {message}")
    if message == "none":
        speak("Sorry, I couldn't understand the message.")
        return
    pyautogui.write(message)
    time.sleep(1)

    # Attachment (optional)
    speak("Do you want to attach a file?")
    update_conversation("Assistant: Do you want to attach a file? Say yes or no.")
    choice = takeCommand()
    update_conversation(f"User: {choice}")

    if "yes" in choice:
        speak("Say the file name with extension from the downloads folder.")
        update_conversation("Assistant: Waiting for file name...")
        filename = takeCommand().replace(" ", "")
        update_conversation(f"User: {filename}")
        filepath = os.path.join(os.path.expanduser("~"), "Downloads", filename)

        # Press attachment button using shortcut (Shift + Tab to focus on bottom bar, then Enter)
        pyautogui.hotkey("ctrl", "shift", "a")  # works on some setups
        time.sleep(3)

        pyautogui.write(filepath)
        pyautogui.press("enter")
        time.sleep(5)
        update_conversation("Assistant: File attached.")

    # Send email
    pyautogui.hotkey("ctrl", "enter")
    speak("Email sent successfully.")
    update_conversation("Assistant: Email sent successfully.")

# Dummy test
if __name__ == "__main__":
    def dummy(text): print(text)
    send_gmail(dummy)
