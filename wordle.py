'''Functions for manipulating the in-memory dictionary and checking word results
'''
import sys
from wordle_dict import *
import argparse as arg
import logging
import log_config  # import does logging config
from wordle_util import check_word
from wordle_strategies import build_strategy_from_name
from wordle_strategy import default_exploration_settings

log = logging.getLogger(__name__)


def main():
    parser = arg.ArgumentParser(
        description="Computer plays a game of Wordle against itself")
    parser.add_argument("-s", "--solution", type=str, required=True,
                        help="Optionally specify the solution word for the computer to guess")
    parser.add_argument("-t", "--strategy", type=str, default="CombinedWordScore",
                        help="Select a solver strategy, either LetterFrequency, LetterFrequencyList, WordFrequency, or CombinedWordScore")
    parser.add_argument("-g", "--guesses", type=int, default=None, required=False,
                        help="Number of exploration guesses to use for strategies that support it")
    args = parser.parse_args()

    solution = args.solution
    exploration_settings = default_exploration_settings()

    if args.guesses is not None:
        exploration_settings["max_guesses"] = args.guesses

    strat = build_strategy_from_name(args.strategy, exploration_settings)

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
