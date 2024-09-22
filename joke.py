import random
import os
import pyttsx3
import speech_recognition as sr

class JokeTeller:
    def __init__(self):
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the computer go to the doctor? Because it had a virus!",
            "Why do cows have hooves instead of feet? Because they lactose.",
            "Why was the math book sad? It had too many problems.",
            "Why did the scarecrow win an award? Because he was outstanding in his field.",
            "What do you get when you cross a snowman and a vampire? Frostbite.",
            "Why don’t skeletons fight each other? They don’t have the guts.",
            "Why did the bicycle fall over? It was two-tired!",
            "How do you organize a space party? You planet!",
            "What’s orange and sounds like a parrot? A carrot!",
            "What do you call fake spaghetti? An impasta.",
            "Why can’t you give Elsa a balloon? Because she will let it go.",
            "What did one plate say to the other? Lunch is on me!",
            "Why do fish live in salt water? Because pepper makes them sneeze!",
            "What’s brown and sticky? A stick.",
            "What do you call a belt made out of watches? A waist of time.",
            "Why don’t seagulls fly over the bay? Because then they’d be bagels!",
            "Why did the golfer bring two pairs of pants? In case he got a hole in one.",
            "Why don’t eggs tell jokes? They’d crack each other up.",
            "Why couldn’t the bicycle stand up by itself? It was two-tired.",
            "What do you call cheese that isn't yours? Nacho cheese!",
            "Why did the tomato turn red? Because it saw the salad dressing!",
            "Why did the banana go to the doctor? Because it wasn’t peeling well!",
            "Why don’t sharks like fast food? Because they can’t catch it!",
            "Why are ghosts bad at lying? You can see right through them!",
            "How do you catch a squirrel? Climb a tree and act like a nut!",
            "Why did the coffee file a police report? It got mugged.",
            "What do you call a pig that does karate? A pork chop!",
            "Why don’t dinosaurs talk? Because they’re extinct!",
            "Why was the big cat disqualified from the race? Because it was a cheetah.",
            "What’s the best way to watch a fly fishing tournament? Live stream it.",
            "Why did the teddy bear say no to dessert? Because he was already stuffed.",
            "Why can’t you trust stairs? They’re always up to something.",
            "How do you make a tissue dance? You put a little boogie in it.",
            "Why are elevator jokes so good? They work on so many levels.",
            "Why don’t you play cards in the jungle? Too many cheetahs.",
            "Why was the belt arrested? It was holding up a pair of pants.",
            "What did the ocean say to the shore? Nothing, it just waved.",
            "What do you call an alligator in a vest? An investigator."
        ]
        self.seen_jokes = set()
        self.load_seen_jokes()
        self.engine = pyttsx3.init("sapi5")
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  
        self.engine.setProperty("rate", 170)

    def load_seen_jokes(self):
        """Load jokes from the joke.txt file."""
        if os.path.exists("joke.txt"):
            with open("joke.txt", "r") as file:
                self.seen_jokes = set(file.read().splitlines())

    def save_joke(self, joke):
        """Append the joke to the joke.txt file."""
        with open("joke.txt", "a") as file:
            file.write(joke + "\n")

    def clear_history(self):
        """Clear the joke history."""
        with open("joke.txt", "w") as file:  
            file.truncate()  
        self.seen_jokes.clear()  
        print("Joke history cleared.")
        self.speak("Joke history cleared.")

    def fetch_joke(self):
        """Fetch a new joke that hasn't been seen yet."""
        available_jokes = [joke for joke in self.jokes if joke not in self.seen_jokes]
        
        if not available_jokes:
            self.clear_history()  
            available_jokes = self.jokes

        joke = random.choice(available_jokes)
        self.seen_jokes.add(joke)
        return joke

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

    def ask_next_or_exit(self):
        """Ask if the user wants to hear the next joke or exit."""
        self.speak("Would you like to hear the next joke or stop?")
        command = self.take_command()
        if "next" in command:
            return True
        elif "stop" in command:
            return False
        else:
            self.speak("Sorry, I didn't catch that. Please say 'next' or 'stop'.")
            return self.ask_next_or_exit()

    def ask_to_save(self, joke):
        """Ask if the user wants to save the joke to the history."""
        self.speak("Would you like to save this joke?")
        command = self.take_command()
        if "yes" in command:
            self.save_joke(joke)
            self.speak("Joke saved.")
        elif "no" in command:
            self.speak("Joke not saved.")
        else:
            self.speak("Sorry, I didn't catch that. Please say 'yes' or 'no'.")
            self.ask_to_save(joke)


if __name__ == "__main__":
    joke_teller = JokeTeller()

    while True:
        joke = joke_teller.fetch_joke()
        print(joke)
        joke_teller.speak(joke)
        
        joke_teller.ask_to_save(joke)  

        if not joke_teller.ask_next_or_exit():  
            break

    joke_teller.speak("Goodbye!")
