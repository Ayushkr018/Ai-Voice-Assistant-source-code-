import requests
from datetime import datetime, timedelta
import json
import threading
from playsound import playsound
import pyttsx3
import speech_recognition as sr

# Calendarific API details
API_KEY = "esvssrUtUpn85a7JvTnO5w1EnpdnJ2DT"  # Replace with your API key from Calendarific
BASE_URL = "https://calendarific.com/api/v2/holidays"

class Calendar:
    def __init__(self):
        self.events = {}  # Dictionary to hold events
        self.engine = pyttsx3.init("sapi5")
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # Set to female voice or change index as per requirement
        self.engine.setProperty("rate", 170)

    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def take_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print("Understanding...")
            query = r.recognize_google(audio, language='en-in')
            print(f"You Said: {query}\n")
            return query.lower()
        except Exception:
            print("Say that again...")
            return "none"

    def tell_today_date(self):
        today = datetime.now().strftime("%A, %B %d, %Y")
        self.speak(f"Today is {today}")
    
    def ask_for_today_date(self):
        self.speak("Do you want to know today's date?")
        response = self.take_command()
        if "yes" in response or "sure" in response:
            self.tell_today_date()
        else:
            self.speak("Okay!")

    def add_event(self):
        """Add a new event using voice commands."""
        self.speak("Tell me the date for the event in YYYY-MM-DD format.")
        date = self.take_command()
        self.speak("Tell me the time for the event in HH:MM format.")
        time = self.take_command()
        self.speak("What is the event description?")
        description = self.take_command()
        self.speak("What is the category for this event, like work or personal?")
        category = self.take_command()
        self.speak("Is this a recurring event? Say daily, weekly, monthly, or none.")
        recurring = self.take_command().strip().lower()
        recurring = None if recurring == 'none' else recurring

        datetime_str = f"{date} {time}"
        event_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        self.events[event_time] = {'description': description, 'category': category, 'recurring': recurring}
        print(f"Event added: {description} on {event_time} (Category: {category}, Recurring: {recurring})")
        self.speak(f"Event added: {description} on {event_time}")

    def view_events(self):
        """View events using voice commands."""
        if not self.events:
            self.speak("No events scheduled.")
            return

        self.speak("Do you want to filter events by category?")
        response = self.take_command()
        category = None
        if "yes" in response:
            self.speak("Tell me the category name.")
            category = self.take_command()

        if category:
            filtered_events = {time: details for time, details in self.events.items() if details['category'] == category}
            if not filtered_events:
                self.speak(f"No events found in the '{category}' category.")
                return
            self.speak(f"Here are the events in the '{category}' category.")
            for event_time, details in sorted(filtered_events.items()):
                self.speak(f"On {event_time}, you have {details['description']}.")
        else:
            self.speak("Here are all your events.")
            for event_time, details in sorted(self.events.items()):
                self.speak(f"On {event_time}, you have {details['description']}.")

    def delete_event(self):
        """Delete an event using voice commands."""
        self.speak("Tell me the date of the event in YYYY-MM-DD format.")
        date = self.take_command()
        self.speak("Tell me the time of the event in HH:MM format.")
        time = self.take_command()
        datetime_str = f"{date} {time}"
        event_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        if event_time in self.events:
            del self.events[event_time]
            self.speak(f"Event on {event_time} deleted.")
        else:
            self.speak("No such event found.")

    def set_reminder(self):
        """Set a reminder using voice commands."""
        self.speak("Tell me the date of the event in YYYY-MM-DD format.")
        date = self.take_command()
        self.speak("Tell me the time of the event in HH:MM format.")
        time = self.take_command()
        self.speak("How many minutes before the event do you want to be reminded?")
        reminder_minutes = int(self.take_command())
        
        datetime_str = f"{date} {time}"
        event_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        if event_time in self.events:
            reminder_time = event_time - timedelta(minutes=reminder_minutes)
            self.speak(f"Reminder set for {reminder_time}.")
            threading.Timer((reminder_time - datetime.now()).total_seconds(), self.trigger_reminder, args=(event_time,)).start()
        else:
            self.speak("No such event found to set a reminder.")

    def trigger_reminder(self, event_time):
        """Trigger a reminder."""
        event = self.events.get(event_time)
        if event:
            self.speak(f"Reminder: Your event {event['description']} is starting soon!")
            playsound('reminder_sound.mp3')

    def get_indian_festivals(self):
        """Fetch Indian festivals using Calendarific API."""
        year = datetime.now().year
        url = f"{BASE_URL}?api_key={API_KEY}&country=IN&year={year}&type=festival"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                festivals = data['response']['holidays']
                self.speak(f"Festivals in India for {year}:")
                for festival in festivals:
                    name = festival['name']
                    date = festival['date']['iso']
                    description = festival['description']
                    self.speak(f"{name} on {date}: {description}")
            else:
                self.speak("Failed to fetch festivals.")
        except requests.exceptions.RequestException as e:
            self.speak("Error fetching festivals.")

# Example of how to use the Calendar class
if __name__ == "__main__":
    calendar = Calendar()

    while True:
        calendar.speak("What would you like to do? You can add an event, view events, delete an event, set a reminder, or ask for today's date.")
        action = calendar.take_command()

        if "add event" in action:
            calendar.add_event()

        elif "view events" in action:
            calendar.view_events()

        elif "delete event" in action:
            calendar.delete_event()

        elif "set reminder" in action:
            calendar.set_reminder()

        elif "today's date" in action or "tell me the date" in action:
            calendar.tell_today_date()

        elif "exit" in action or "quit" in action:
            calendar.speak("Goodbye!")
            break

        else:
            calendar.speak("I didn't understand that. Please try again.")
