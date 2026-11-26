
import random

words = [
    "python", "computer", "programming", "keyboard",
    "internet", "science", "student", "technology",
    "developer", "education", "software", "hangman"
]

word = random.choice(words)
guessed = []
attempts = 6

print("WELCOME TO HANGMAN GAME!")

while attempts > 0:
    display = ""

    for letter in word:
        if letter in guessed:
            display += letter + " "
        else:
            display += "_ "

    print("\nWord:", display)
    print("Attempts left:", attempts)

    if all(letter in guessed for letter in word):
        print("Congratulations! You won!")
        break

    guess = input("Guess a letter: ").lower()

    if len(guess) != 1 or not guess.isalpha():
        print("Please enter only one letter.")
        continue

    if guess in guessed:
        print("You already guessed this letter!")
        continue

    guessed.append(guess)

    if guess not in word:
        attempts -= 1
        print("Wrong guess!")

if attempts == 0:
    print("Game over! The word was:", word)
