from deep_translator import GoogleTranslator
from gtts import gTTS
from gtts.lang import tts_langs
import pyttsx3
import speech_recognition as sr
import os
from playsound import playsound
import time

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
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, timeout=4)

    try:
        print("Understanding..")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except Exception:
        print("Say that again...")
        return "None"
    return query

def get_language_code():
    speak("Please name the language you want to translate to.")
    language_query = takeCommand().lower()

    try:
        supported_langs = GoogleTranslator(source='auto', target='en').get_supported_languages()
        normalized_langs = {lang.lower(): lang for lang in supported_langs}

        if language_query in normalized_langs:
            return normalized_langs[language_query]
        else:
            speak("Sorry, that language is not supported.")
            return None
    except Exception as e:
        print(f"Error fetching supported languages: {e}")
        speak("An error occurred while checking supported languages.")
        return None

def translategl(query, update_conversation):
    speak("Sure, Sir")

    lang_code = None
    while not lang_code:
        lang_code = get_language_code()

    try:
        translated_text = GoogleTranslator(source='auto', target=lang_code).translate(query)
        print(f"Translated Text: {translated_text}")
        speak(f"The translation is: {translated_text}")
        update_conversation(f"Assistant: The translation is: {translated_text}")

        try:
            supported_tts_langs = tts_langs()
            tts_lang = 'en' if lang_code not in supported_tts_langs else lang_code
            speakgl = gTTS(text=translated_text, lang=tts_lang, slow=False)
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
