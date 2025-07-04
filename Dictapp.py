import os
import webbrowser
import pyttsx3

# Initialize the speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 200)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Dictionary for apps and their command to open
dictapp = {
    "commandprompt": "cmd",
    "paint": "mspaint",
    "word": "winword",
    "excel": "excel",
    "chrome": "chrome",
    "vscode": "code",
    "powerpoint": "powerpnt"
}

# Function to open an app or website
def openappweb(query, update_conversation):
    speak("Launching, sir")
    update_conversation(f"Assistant: Launching {query.strip()}")

    # Check if it's a website
    if ".com" in query or ".co.in" in query or ".org" in query:
        query = query.replace("open", "").replace("launch", "").strip()
        webbrowser.open(f"https://www.{query}")
        update_conversation(f"Assistant: Opening {query}")
    
    # Otherwise, check if it's an app
    else:
        keys = dictapp.keys()
        for app in keys:
            if app in query:
                speak(f"Opening {app}")
                os.system(f"start {dictapp[app]}")
                update_conversation(f"Assistant: Opening {app}")
                break
        else:
            speak("Application not found")
            update_conversation(f"Assistant: Application {query.strip()} not found")

# Function to close an app
def closeappweb(query, update_conversation):
    speak("Closing, sir")
    update_conversation(f"Assistant: Closing {query.strip()}")

    # Handling app closure
    keys = dictapp.keys()
    for app in keys:
        if app in query:
            speak(f"Closing {app}")
            os.system(f"taskkill /f /im {dictapp[app]}.exe")
            update_conversation(f"Assistant: Closing {app}")
            break
    else:
        speak("Application not found")
        update_conversation(f"Assistant: Application {query.strip()} not found")
