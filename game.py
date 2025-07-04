import random
import time
import pyttsx3


def speak(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

# Trivia quiz game
def trivia_quiz(num_players, update_conversation):
    questions = [
        {"question": "What is the capital of France?", "answer": "paris"},
        # Add more questions...
    ]

    scores = [0] * num_players
    for i in range(10):
        question = random.choice(questions)
        for player in range(num_players):
            speak(f"Player {player + 1}, {question['question']}")
            answer = input(f"Player {player + 1}, Your answer: ").lower()

            if answer == question["answer"]:
                scores[player] += 1
                speak("Correct!")
                update_conversation(f"Player {player + 1} answered correctly.")
            else:
                speak(f"Wrong! The correct answer is {question['answer']}.")
                update_conversation(f"Player {player + 1} answered incorrectly.")

    speak("Quiz over! Here are the final scores:")
    for player, score in enumerate(scores):
        speak(f"Player {player + 1}: {score} points.")
        update_conversation(f"Player {player + 1}: {score} points.")

# Guess the Word game
def guess_the_word(num_players, update_conversation):
    words = ["apple", "banana", "grape", "orange"]
    scores = [0] * num_players

    for player in range(num_players):
        word = random.choice(words)
        attempts = 3
        speak(f"Player {player + 1}, it's your turn! You have {attempts} attempts to guess the word.")
        while attempts > 0:
            guess = input(f"Player {player + 1}, guess the word: ").lower()
            if guess == word:
                scores[player] += 1
                speak("Correct! You guessed the word!")
                update_conversation(f"Player {player + 1} guessed the word correctly.")
                break
            attempts -= 1
            if attempts > 0:
                speak("Wrong guess! Try again.")
                update_conversation(f"Player {player + 1} guessed wrong.")

    speak("Game over! Here are the final scores:")
    for player, score in enumerate(scores):
        speak(f"Player {player + 1}: {score} points.")
        update_conversation(f"Player {player + 1}: {score} points.")

# Rock-paper-scissors game
def rock_paper_scissors(num_players, update_conversation):
    choices = ["rock", "paper", "scissors"]
    scores = [0] * num_players

    for player in range(num_players):
        user_score = 0
        computer_score = 0
        speak(f"Player {player + 1}, it's your turn!")

        for _ in range(3):  # Best of 3 rounds
            user_choice = input("Choose rock, paper, or scissors: ").lower()
            computer_choice = random.choice(choices)
            speak(f"Computer chose: {computer_choice}")

            if user_choice == computer_choice:
                speak("It's a tie!")
                update_conversation(f"Player {player + 1}: It's a tie!")
            elif (user_choice == "rock" and computer_choice == "scissors") or \
                 (user_choice == "paper" and computer_choice == "rock") or \
                 (user_choice == "scissors" and computer_choice == "paper"):
                speak("You win this round!")
                user_score += 1
                update_conversation(f"Player {player + 1} wins this round!")
            else:
                speak("Computer wins this round!")
                computer_score += 1
                update_conversation(f"Computer wins this round!")

        if user_score > computer_score:
            speak(f"You win the game! Final score: {user_score}-{computer_score}")
            scores[player] += 1
        else:
            speak(f"Computer wins the game! Final score: {computer_score}-{user_score}")

    speak("Rock-paper-scissors game over!")

# Tic-tac-toe game
def tic_tac_toe(num_players, update_conversation):
    # Implement the tic-tac-toe game logic and add update_conversation calls as needed
    pass

# Main game function
def game_play(update_conversation):
    speak("Welcome to the game section! Would you like to play single-player or multiplayer?")
    mode = input("Type 'single' for single-player or 'multi' for multiplayer: ").lower()

    if mode == "multi":
        speak("How many players? You can choose between 2, 3, or 4 players.")
        num_players = int(input("Enter number of players (2-4): "))
    else:
        num_players = 1

    speak("Which game would you like to play? Trivia Quiz, Guess the Word, Rock-paper-scissors, or Tic Tac Toe?")
    choice = input("Your choice: ").lower()

    if "trivia" in choice:
        trivia_quiz(num_players, update_conversation)
    elif "guess" in choice:
        guess_the_word(num_players, update_conversation)
    elif "rock" in choice:
        rock_paper_scissors(num_players, update_conversation)
    elif "tic" in choice:
        tic_tac_toe(num_players, update_conversation)
    else:
        speak("Sorry, I don't recognize that game.")

# Example usage
if __name__ == "__main__":
    # Add the update_conversation function for GUI logging
    def update_conversation(text):
        print(text)  # Replace with your GUI update code

    game_play(update_conversation)
