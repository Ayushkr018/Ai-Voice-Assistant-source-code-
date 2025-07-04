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
}

def speak(audio, update_conversation=None):
    engine.say(audio)
    engine.runAndWait()
    if update_conversation:
        update_conversation("Assistant: " + audio)

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

def fetch_news_from_gnews(sector, country, update_conversation):
    keyword = sector_keywords.get(sector, "")
    url = f"https://gnews.io/api/v4/top-headlines?lang={country}&topic={keyword}&token=7de488784d56ac7ee0b21fcaf1960215"

    try:
        response = requests.get(url)
        data = response.json()
        articles = data.get("articles", [])

        if not articles:
            speak(f"No articles found for {sector} in {country}.", update_conversation)
            return

        speak(f"Here is the news for {sector} in {country}.", update_conversation)
        for i, article in enumerate(articles):
            title = article.get("title", "No title available")
            news_url = article.get("url", "No URL available")
            print(f"Title: {title}\nURL: {news_url}")

            speak(f"News {i + 1}: {title}. For more info, visit the URL.", update_conversation)

            speak("Say 'next' to continue, 'change' to switch sector, or 'leave it' to stop.", update_conversation)
            command = takeCommand()

            if command == "leave it":
                speak("Stopping news updates.", update_conversation)
                return
            elif command == "change":
                speak("Switching sector.", update_conversation)
                break
            elif command == "next":
                if i == len(articles) - 1:
                    speak(f"No more articles available for {sector} in {country}.", update_conversation)
                    break
                continue
            else:
                speak("Command not recognized, moving to the next article.", update_conversation)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news from GNews: {e}")
        speak(f"Sorry, there was an issue fetching news for {sector} in {country}. Please try again later.", update_conversation)

def latestnews(update_conversation):
    while True:
        speak("Which sector do you want news from? Choose from business, sports, political, health, technology, or science.", update_conversation)
        sector = takeCommand()

        if sector == "stop":
            speak("Stopping news updates.", update_conversation)
            break
        elif sector not in sector_keywords:
            speak(f"Sorry, I couldn't find any news field for {sector}. Please try another category.", update_conversation)
            continue

        speak("Which country do you want news from? Please say the full name of the country.", update_conversation)
        country = takeCommand()

        if country == "stop":
            speak("Stopping news updates.", update_conversation)
            break

        preferences['sector'] = sector
        preferences['country'] = country
        fetch_news_from_gnews(sector, country, update_conversation)

def notify_news(update_conversation):
    sector = preferences.get('sector', 'business')
    country_code = preferences.get('country', 'us')
    fetch_news_from_gnews(sector, country_code, update_conversation)

def run_schedule(update_conversation):
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_schedule, args=(None,), daemon=True).start()
