import pyautogui
import pyttsx3
import speech_recognition as sr
import time
import os

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
        r.energy_threshold = 200
        audio = r.listen(source)

    try:
        print("Understanding...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again...")
        return "None"
    return query.lower()

def open_whatsapp_desktop():
    pyautogui.hotkey('win', 's')
    time.sleep(1)
    pyautogui.write('WhatsApp') 
    time.sleep(1)
    pyautogui.press('enter')  
    time.sleep(5)
      
def close_whatsapp():
    os.system("taskkill /f /im WhatsApp.exe")
    
def sendMessage():
    open_whatsapp_desktop()

    speak("Who do you want to message? You can say the name of a contact or group.")
    recipient = takeCommand()

    if recipient == "None":
        speak("Sorry, I didn't catch the name. Please try again.")
        return

    speak("What message do you want to send?")
    message = takeCommand()

    if message == "None":
        speak("Sorry, I didn't catch the message. Please try again.")
        return

    pyautogui.hotkey('ctrl', 'f')  
    time.sleep(1)
    pyautogui.write(recipient)  
    time.sleep(2) 

    pyautogui.press('down') 
    time.sleep(1)
    pyautogui.press('enter') 
    time.sleep(2)


    pyautogui.write(message) 
    time.sleep(1)
    pyautogui.press('enter')  

    speak("Message sent.")
    
    time.sleep(3)
    close_whatsapp()

if __name__ == "__main__":
    sendMessage()
