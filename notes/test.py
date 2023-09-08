""
Generate a random number between 1 and 9 (including 1 and 9).
Ask the user to guess the number, then tell them whether they guessed too low, too high, or exactly right.


import random

# Generate a random number between 1 and 9 (including 1 and 9).
num = random.randint(1, 9)  # Generate a random number between 1 and 9 (including 1 and 9).

# Ask the user to guess the number.
guess = int(input("Guess a number between 1 and 9: "))  