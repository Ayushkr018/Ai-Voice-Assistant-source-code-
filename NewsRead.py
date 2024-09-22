import requests
import pyttsx3
import speech_recognition as sr
import schedule
import time
import threading


engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  
engine.setProperty("rate", 170)

preferences = {
    "sector": "business",  
    "country": "us"        

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


sector_keywords = {
    "business": "business",
    "sports": "sports",
    "political": "politics",
    "health": "health",
    "technology": "technology",
    "science": "science"
}


def fetch_news_from_gnews(sector, country):
    keyword = sector_keywords.get(sector, "")
    url = f"https://gnews.io/api/v4/top-headlines?lang={country}&topic={keyword}&token=YOUR API KEY"

    try:
        response = requests.get(url)
        data = response.json()
        articles = data.get("articles", [])

        if not articles:
            speak(f"No articles found for {sector} in {country}.")
            return

        speak(f"Here is the news for {sector} in {country}.")
        for i, article in enumerate(articles):
            title = article.get("title", "No title available")
            news_url = article.get("url", "No URL available")
            print(f"Title: {title}\nURL: {news_url}")

            speak(f"News {i + 1}: {title}. For more info, visit the URL.")

            speak("Say 'next' to continue, 'change' to switch sector, or 'leave it' to stop.")
            command = takeCommand()

            if command == "leave it":
                speak("Stopping news updates.")
                return
            elif command == "change":
                speak("Switching sector.")
                break
            elif command == "next":
                if i == len(articles) - 1:
                    speak(f"No more articles available for {sector} in {country}.")
                    break
                continue
            else:
                speak("Command not recognized, moving to the next article.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news from GNews: {e}")
        speak(f"Sorry, there was an issue fetching news for {sector} in {country}. Please try again later.")


def notify_news():
    sector = preferences.get('sector', 'business')  
    country_code = preferences.get('country', 'us')  
    fetch_news_from_gnews(sector, country_code)


schedule.every().hour.at(":00").do(notify_news)


def latestnews():
    while True:
        speak("Which sector do you want news from? Choose from business, sports, political, health, technology, or science.")
        sector = takeCommand()

        if sector == "stop":
            speak("Stopping news updates.")
            break
        elif sector not in sector_keywords:
            speak(f"Sorry, I couldn't find any news field for {sector}. Please try another category.")
            continue

        speak("Which country do you want news from? Please say the full name of the country.")
        country = takeCommand()

        if country == "stop":
            speak("Stopping news updates.")
            break

       
        preferences['sector'] = sector
        preferences['country'] = country  

      
        fetch_news_from_gnews(sector, country)


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1) 


threading.Thread(target=run_schedule, daemon=True).start()


if __name__ == "__main__":
    latestnews()
