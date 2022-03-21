'''Functions for manipulating the in-memory dictionary and checking word results
'''
import random
import sys
from wordle_dict import *
import argparse as arg
import logging
import log_config  # import does logging config
from wordle_util import WRONG, CORRECT, MISPLACED, check_word
from quordle_strategy import QuordleStrategy
log = logging.getLogger(__name__)


def main():
    parser = arg.ArgumentParser(
        description="Computer plays a game of Quordle against itself")
    parser.add_argument("-s", "--solutions", type=list[str],
                        help="Optionally specify the solution words for the computer to guess")
    args = parser.parse_args()

    words = load_dictionary()
    solutions: list[str] = args.solutions or [
        random.choice(words) for x in range(0, 4)]

    strat = QuordleStrategy()

    print(f"Solutions are '{solutions}'")

    for guess_num in range(1, 10):
        if all([s is None for s in solutions]):
            print(f"Solved all the words!")
            break

        guess_word = strat.next_guess()
        print(f"For guess {guess_num} I'll try '{guess_word}'")

        all_results = [_check_single_solution(solution, guess_word)
                       for solution in solutions]
        for (idx, (is_correct, letter_scores)) in enumerate(all_results):
            if is_correct is None:
                print(f"Guess {guess_num} word {idx + 1}: already solved!")
            elif is_correct:
                print(
                    f"Guess {guess_num} word {idx + 1}: '{guess_word}' is correct, I win!")
                solutions[idx] = None
            else:
                print(
                    f"Guess {guess_num} word {idx + 1}: '{guess_word}' was wrong, result was '{letter_scores}'")

        strat.accept_results([r[1] for r in all_results])


def _check_single_solution(solution: str, guess_word: str):
    if solution is None:
        return (None, None)
    else:
        return check_word(solution, guess_word)


if __name__ == "__main__":
    sys.exit(main())
