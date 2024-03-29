"""Simple script.

Example usage:
  python guess.py
  python guess.py --minimum 1 --maximum 10 --rounds 3

To see all options:
  python guess.py -h

Any variable that is annotated with `cat.CliArgument` in a `@ptera` function
can be set on the command line. `ptera.auto_cli` will find them automatically.
"""

import random

from ptera import auto_cli, cat, default, ptera


@ptera
def guess():
    # Minimal possible number
    minimum: cat.CliArgument = default(0)
    # Maximal possible number
    maximum: cat.CliArgument = default(100)
    # Maximal number of tries
    maxtries: cat.CliArgument = default(10)

    # Force the number to guess (defaults to random)
    target: cat.CliArgument = default(random.randint(minimum, maximum))

    assert minimum <= target <= maximum

    print(f"> Please guess a number between {minimum} and {maximum}")
    for i in range(maxtries):
        guess = float(input())
        if guess == target:
            print("Yes! :D")
            return True
        elif i == maxtries - 1:
            print("You failed :(")
            return False
        elif guess < target:
            print("> Too low. Guess again.")
        elif guess > target:
            print("> Too high. Guess again.")


@ptera
def main():
    # Number of rounds of guessing
    rounds: cat.CliArgument = default(1)

    for i in range(rounds):
        guess()


if __name__ == "__main__":
    auto_cli(main, description="Guessing game", category=cat.CliArgument)
