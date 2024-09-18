import wolframalpha
import pyttsx3

# Initialize the speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 170)

def speak(audio):
    """Function to make the system speak."""
    engine.say(audio)
    engine.runAndWait()

def WolframAlpha(query):
    """Query WolframAlpha for an answer to a given input query."""
    apikey = "2RAXXJ-AP6X66KU7E"  # Replace with your WolframAlpha API key
    client = wolframalpha.Client(apikey)
    result = client.query(query)

    try:
        answer = next(result.results).text
        return answer
    except StopIteration:
        speak("The value is not answerable")
        return None

def Calc(query):
    """Perform basic arithmetic using WolframAlpha."""
    Term = str(query)
    Term = Term.replace("Eva", "")
    Term = Term.replace("multiply", "*")
    Term = Term.replace("plus", "+")
    Term = Term.replace("minus", "-")
    Term = Term.replace("divide", "/")
    
    try:
        result = WolframAlpha(Term)
        if result:
            print(f"Result: {result}")
            speak(result)
        else:
            speak("Unable to calculate the result.")
    except Exception as e:
        speak("An error occurred: " + str(e))

def main():
    while True:
        query = input("Enter your query or calculation (type 'exit' to quit): ").lower()
        if "exit" in query:
            speak("Goodbye!")
            break
        elif "calculate" in query or "result" in query:
            Calc(query)
        else:
            speak("Sorry, I didn't understand that. Please ask for a calculation.")

if __name__ == "__main__":
    main()
