import random
import time
import pyttsx3

# Initialize the text-to-speech engine
def speak(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

# Trivia quiz game
def trivia_quiz(num_players):
    questions = [
        {"question": "What is the capital of France?", "answer": "paris"},
        {"question": "Who wrote 'Hamlet'?", "answer": "shakespeare"},
        {"question": "What is the chemical symbol for water?", "answer": "h2o"},
        {"question": "What planet is known as the Red Planet?", "answer": "mars"},
        {"question": "What year did the Titanic sink?", "answer": "1912"},
        {"question": "Who was the first man to walk on the moon?", "answer": "neil armstrong"},
        {"question": "Which element has the atomic number 1?", "answer": "hydrogen"},
        {"question": "Who painted the Mona Lisa?", "answer": "leonardo da vinci"},
        {"question": "What is the largest ocean on Earth?", "answer": "pacific"},
        {"question": "What is the smallest prime number?", "answer": "2"},
        {"question": "What is the capital of Japan?", "answer": "tokyo"},
        {"question": "What is the longest river in the world?", "answer": "nile"},
        {"question": "Who discovered penicillin?", "answer": "alexander fleming"},
        {"question": "Which planet is closest to the Sun?", "answer": "mercury"},
        {"question": "What is the hardest natural substance?", "answer": "diamond"},
        {"question": "In what year did World War I start?", "answer": "1914"},
        {"question": "What is the square root of 144?", "answer": "12"},
        {"question": "Who wrote '1984'?", "answer": "george orwell"},
        {"question": "What is the largest mammal?", "answer": "blue whale"},
        {"question": "How many continents are there?", "answer": "7"}
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
            else:
                speak(f"Wrong! The correct answer is {question['answer']}.")
            time.sleep(1)
    
    speak("Quiz over! Here are the final scores:")
    for player, score in enumerate(scores):
        speak(f"Player {player + 1}: {score} points.")

# Guess the Word game
def guess_the_word(num_players):
    words = ["apple", "banana", "grape", "orange", "kiwi", "strawberry", "pineapple", "mango"]
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
                break
            attempts -= 1
            if attempts > 0:
                speak("Wrong guess! Try again.")
            else:
                speak(f"Out of attempts! The correct word was {word}.")
    
    speak("Game over! Here are the final scores:")
    for player, score in enumerate(scores):
        speak(f"Player {player + 1}: {score} points.")

# Rock-paper-scissors game
def rock_paper_scissors(num_players):
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
            elif (user_choice == "rock" and computer_choice == "scissors") or \
                 (user_choice == "paper" and computer_choice == "rock") or \
                 (user_choice == "scissors" and computer_choice == "paper"):
                speak("You win this round!")
                user_score += 1
            else:
                speak("Computer wins this round!")
                computer_score += 1

            time.sleep(1)

        if user_score > computer_score:
            speak(f"You win the game! Final score: {user_score}-{computer_score}")
            scores[player] += 1
        else:
            speak(f"Computer wins the game! Final score: {computer_score}-{user_score}")

    speak("Rock-paper-scissors game over!")

# Tic-tac-toe game
def tic_tac_toe(num_players):
    def print_board(board):
        for row in board:
            print(" | ".join(row))
            print("-" * 5)

    def check_winner(board):
        for row in board:
            if row[0] == row[1] == row[2] and row[0] != " ":
                return row[0]
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
                return board[0][col]
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
            return board[0][2]
        return None

    scores = [0] * num_players
    for player in range(num_players):
        board = [[" " for _ in range(3)] for _ in range(3)]
        current_player = "X"
        speak(f"Player {player + 1}, it's your turn!")

        for _ in range(9):  # Max 9 moves in a tic-tac-toe game
            print_board(board)
            row = int(input(f"Player {current_player}, enter the row (0, 1, 2): "))
            col = int(input(f"Player {current_player}, enter the column (0, 1, 2): "))

            if board[row][col] == " ":
                board[row][col] = current_player
            else:
                speak("Spot already taken, try again.")
                continue

            winner = check_winner(board)
            if winner:
                print_board(board)
                speak(f"Player {winner} wins!")
                scores[player] += 1
                break

            current_player = "O" if current_player == "X" else "X"
        else:
            speak("It's a tie!")

    speak("Tic-tac-toe game over!")

# Main game function
def game_play():
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
        trivia_quiz(num_players)
    elif "guess" in choice:
        guess_the_word(num_players)
    elif "rock" in choice:
        rock_paper_scissors(num_players)
    elif "tic" in choice:
        tic_tac_toe(num_players)
    else:
        speak("Sorry, I don't recognize that game.")

# Example usage
if __name__ == "__main__":
    game_play()
