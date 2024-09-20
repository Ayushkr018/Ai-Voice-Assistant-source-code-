from googletrans import Translator, LANGUAGES
from gtts import gTTS
import pyttsx3
import speech_recognition as sr
import os
from playsound import playsound
import time

# Initialize pyttsx3 engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Use the Narrator voice (index 1)
engine.setProperty("rate", 170)  # Set speech rate

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Take voice command function
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, timeout=4)

    try:
        print("Understanding..")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again...")
        return "None"
    return query

# Function to get voice input for language code
def get_language_code():
    speak("Please name the language you want to translate to.")
    print(LANGUAGES)  # Display available languages
    language_query = takeCommand().lower()
    
    # Match spoken language to language code
    for lang_code, lang_name in LANGUAGES.items():
        if lang_name.lower() == language_query:
            return lang_code

    speak("Sorry, I couldn't understand the language. Please try again.")
    return None

# Translate and speak function
def translategl(query):
    speak("Sure, Sir")
    translator = Translator()

    # Get the destination language via voice
    lang_code = None
    while not lang_code:
        lang_code = get_language_code()

    # Translate the text
    try:
        text_to_translate = translator.translate(query, src="auto", dest=lang_code)
        translated_text = text_to_translate.text
        print(f"Translated Text: {translated_text}")
        speak(f"The translation is: {translated_text}")
        
        # Attempt to convert translated text to speech
        try:
            speakgl = gTTS(text=translated_text, lang=lang_code, slow=False)
            speakgl.save("voice.mp3")
            playsound("voice.mp3")
            time.sleep(1)
            os.remove("voice.mp3")
        except Exception as tts_error:
            print(f"Error with text-to-speech: {tts_error}")
            speak("Unable to convert text to speech.")
    
    except Exception as translate_error:
        print(f"Translation error: {translate_error}")
        speak("Unable to translate the text.")

# Example usage
if __name__ == "__main__":
    speak("How can I assist you today?")
    query = takeCommand()
    if query != "None":
        translategl(query)
