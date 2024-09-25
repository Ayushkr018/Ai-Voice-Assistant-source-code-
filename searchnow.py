import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import webbrowser

# Initialize the speech engine and set to a specific voice
engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Use the Narrator voice (index 1)
engine.setProperty("rate", 170)  # Set speech rate

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 200
        audio = r.listen(source, 0, 4)
    try:
        print("Understanding..")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query.lower()

def searchGoogle(query):
    if "google" in query:
        import wikipedia as googleScrap
        query = query.replace("jarvis", "")
        query = query.replace("google search", "")
        query = query.replace("google", "")
        speak("This is what I found on Google")
        try:
            pywhatkit.search(query)
            result = googleScrap.summary(query, 1)
            speak(result)
        except:
            speak("No speakable output available")

def searchYoutube(query):
    if "youtube" in query:
        speak("This is what I found for your search!") 
        query = query.replace("youtube search", "")
        query = query.replace("youtube", "")
        query = query.replace("jarvis", "")
        web = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(web)
        pywhatkit.playonyt(query)
        speak("Done, Sir")

def searchWikipedia(query):
    if "wikipedia" in query:
        speak("Searching Wikipedia....")
        query = query.replace("wikipedia", "").replace("search wikipedia", "").replace("jarvis", "")
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia..")
            print(results)
            speak(results)
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle the case where the query is ambiguous
            speak("The query is too ambiguous. Here are some options:")
            options = e.options[:5]  # Limit the number of options shown
            for option in options:
                speak(option)
            print("DisambiguationError:", e)
        except wikipedia.exceptions.PageError as e:
            speak("Sorry, I couldn't find a page for that topic.")
            print("PageError:", e)
        except Exception as e:
            speak("An error occurred while searching Wikipedia.")
            print("General Exception:", e)

if __name__ == "__main__":
    while True:
        query = takeCommand()

        if "google" in query:
            searchGoogle(query)
        elif "youtube" in query:
            searchYoutube(query)
        elif "wikipedia" in query:
            searchWikipedia(query)
        else:
            speak("Sorry, I don't have a response for that.")
