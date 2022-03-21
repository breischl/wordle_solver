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
from wordle_strategy import WordleStrategy
log = logging.getLogger(__name__)


def main():
    parser = arg.ArgumentParser(
        description="Computer plays a game of Wordle against itself")
    parser.add_argument("-s", "--solution", type=str,
                        help="Optionally specify the solution word for the computer to guess")
    parser.add_argument("-w", "--wordscorer", type=str, default="PositionalFrequency",
                        choices=["PositionalFrequency", "GlobalFrequency"])
    parser.add_argument("-e", "--exploration", default=5, type=int,
                        help="Number of guesses to remain in exploration mode")
    args = parser.parse_args()

    words = load_dictionary()
    solution = args.solution or random.choice(words)

    settings = {
        "max_guesses": args.exploration
    }

    if(args.wordscorer == "PositionalFrequency"):
        scorer = pfs.PositionalFrequencyWordScorer()
    elif(args.wordscorer == "GlobalFrequency"):
        scorer = gfs.GlobalFrequencyWordScorer()
    else:
        print(f"Unknown word scorer: {args.wordscorer}")
        quit()

    strat = WordleStrategy(word_scorer=scorer, exploration_settings=settings)

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
