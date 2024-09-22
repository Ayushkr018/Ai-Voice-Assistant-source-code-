import wolframalpha
import pyttsx3
import requests
import speech_recognition as sr
import re

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 170)

def speak(audio):
    """Function to make the system speak."""
    engine.say(audio)
    engine.runAndWait()

def take_command():
    """Listen for a command and return it as a string."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Understanding...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except Exception as e:
        print("Say that again...")
        return "None"
    return query.lower()

def WolframAlpha(query):
    """Query WolframAlpha for an answer to a given input query."""
    apikey = ""  # Replace with your WolframAlpha API key
    client = wolframalpha.Client(apikey)
    result = client.query(query)

    try:
        answer = next(result.results).text
        return answer
    except StopIteration:
        speak("The value is not answerable.")
        return None

def currency_conversion(amount, from_currency, to_currency, api_key):
    """Convert currency using Open Exchange Rates."""
    url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}&base={from_currency}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and 'rates' in data:
        conversion_rate = data['rates'].get(to_currency)
        if conversion_rate:
            converted_amount = amount * conversion_rate
            return converted_amount
        else:
            speak("Currency conversion rate not available.")
            return None
    else:
        speak("Error fetching currency data.")
        return None

def clean_amount(amount_str):
    """Remove currency symbols and return a float."""
    amount_str = re.sub(r'[^\d.]+', '', amount_str) 
    return float(amount_str) if amount_str else 0.0

def Calc(query, api_key):
    """Perform calculations and conversions."""
    Term = str(query)

    if "square" in Term:
        number = float(Term.split()[-1])
        result = number ** 2
        speak(f"The square of {number} is {result}.")
    elif "square root" in Term or "what is the square root of" in Term:
        # 
        match = re.search(r'square root of (\d+)', Term)
        if match:
            number = float(match.group(1))
            result = number ** 0.5
            speak(f"The square root of {number} is {result}.")
        else:
            speak("Please specify a number to calculate the square root.")
    elif "currency" in Term or "convert" in Term:
        parts = Term.split()
        amount = clean_amount(parts[1])
        from_currency = parts[3].upper()  
        to_currency = "INR" if "indian rupees" in Term else parts[5].upper()  
        result = currency_conversion(amount, from_currency, to_currency, api_key)
        if result:
            speak(f"{amount} {from_currency} is approximately {result:.2f} {to_currency}.")
    elif "calculate" in Term or "result" in Term:
        result = WolframAlpha(Term)
        if result:
            speak(result)

def main():
    api_key = ""  # Replace with your Open Exchange Rates API key
    speak("Welcome to the calculation assistant. You can ask me to calculate, convert currency, or find square and square root.")
    
    while True:
        speak("Please say your query or calculation.")
        query = take_command()
        
        if "exit" in query:
            speak("Goodbye!")
            break
        
        Calc(query, api_key)

if __name__ == "__main__":
    main()
