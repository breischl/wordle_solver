'''Functions for manipulating the in-memory dictionary and checking word results
'''
import random
import sys
from wordle_dict import *
from word_frequency_strategy import WordFrequencyStrategy
import argparse as arg
import logging
import log_config  # import does logging config
from wordle_util import WRONG, CORRECT, MISPLACED, check_word
from letter_frequency_strategy import WordleLetterFrequencyStrategy
log = logging.getLogger(__name__)


def main():
    parser = arg.ArgumentParser(
        description="Computer plays a game of Wordle against itself")
    parser.add_argument("-s", "--solution", type=str,
                        help="Optionally specify the solution word for the computer to guess")
    parser.add_argument("-t", "--strategy", type=str, default="LetterFrequencyStrategy",
                        help="Select a solver strategy, either LetterFrequencyStrategy or WordFrequencyStrategy")
    parser.add_argument("-g", "--guesses", type=int, default=4,
                        help="Number of exploration guesses to use for LetterFrequencyStrategy")
    args = parser.parse_args()

    solution = args.solution
    strat = WordleLetterFrequencyStrategy(
        exploration_settings={"max_guesses": args.guesses})

    if args.strategy == "WordFrequencyStrategy":
        strat = WordFrequencyStrategy()

    print(f"Solution is '{solution}'")

    for guess_num in range(1, 7):
        guess_word = strat.next_guess()
        if not guess_word:
            print("I have no other ideas, sorry!")
            exit()

        (is_correct, letter_scores) = check_word(solution, guess_word)

        if is_correct:
            print(f"'{guess_word}' is correct, I win!")
            break

        print(f"'{guess_word}' was wrong")
        strat.accept_result(letter_scores, guess_word)


if __name__ == "__main__":
    sys.exit(main())
