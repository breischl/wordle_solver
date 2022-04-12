'''Functions for manipulating the in-memory dictionary and checking word results
'''
import random
import sys
from wordle_dict import *
import positional_frequency_scorer as pfs
import global_frequency_scorer as gfs
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
    args = parser.parse_args()

    solution = args.solution
    strat = WordleLetterFrequencyStrategy()

    print(f"Solution is '{solution}'")

    for guess_num in range(1, 7):
        guess_word = strat.next_guess()

        (is_correct, letter_scores) = check_word(solution, guess_word)

        if is_correct:
            print(f"'{guess_word}' is correct, I win!")
            break

        print(f"'{guess_word}' was wrong")
        strat.accept_result(letter_scores)


if __name__ == "__main__":
    sys.exit(main())
