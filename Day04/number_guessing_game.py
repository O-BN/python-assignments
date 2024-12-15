import random

def generate_answer():
    """Generate a random number between 1 and 20."""
    return random.randint(1, 20)

def get_user_input(answer):
    """Prompt the user to guess a number, validate input, and allow exit or special commands."""
    while True:
        guess = input("Guess the number between 1 and 20 (or type 'x' to exit, 'n' to skip, 's' to show the answer): ").strip().lower()
        if guess == 'x':
            return 'x'
        elif guess == 'n':
            return 'n'
        elif guess == 's':
            print(f"The number is {answer}")
            continue
        try:
            guess = int(guess)
            if 1 <= guess <= 20:
                return guess
            else:
                print("The number must be between 1 and 20.")
        except ValueError:
            print("Please enter a number between 1 and 20, or 'x' to exit.")

def game_loop():
    """Run the main guessing game loop."""
    answer = generate_answer()
    answer_counter = 0
    print("A new number has been generated!")
    while True:
        user_guess = get_user_input(answer)
        if user_guess == 'x':
            print("Exiting the game. Thanks for playing!")
            break
        elif user_guess == 'n':
            print("Skipping this round. Generating a new number...")
            answer = generate_answer()
            continue
        answer_counter += 1
        if user_guess < answer:
            print("Your guess is too low. Try again.")
        elif user_guess > answer:
            print("Your guess is too high. Try again.")
        else:
            print(f"Congratulations! You guessed the correct number! \nIt took you {answer_counter} guesses.")
            break

def play_again():
    """Ask the user if they want to play another round."""
    while True:
        response = input("Would you like to play again? (yes/no): ").strip().lower()
        if response == "yes":
            game_loop()
        elif response == "no":
            print("Thanks for playing! Goodbye!")
            break
        else:
            print("Please enter 'yes' or 'no'.")

def main():
    """Start the guessing game."""
    game_loop()
    play_again()

main()
