'''Functions for manipulating the in-memory dictionary and checking word results
'''
import random
import sys
from wordle_dict import *
import positional_frequency_scorer as pfs
import global_frequency_scorer as gfs
import argparse as arg
from wordle_strategy import WRONG, WordleStrategy
from wordle_strategy import MISPLACED
from wordle_strategy import CORRECT
import log_config
import logging

log = logging.getLogger(__name__)


def check_word(solution: str, guess: str) -> tuple[bool, list[str]]:
    '''Check whether a given guess matches the expected solution, and return that along with match scores for each letter.


    Returns: (is_correct : bool, letter_scores : list[str])
    '''
    if solution == guess:
        return (True, [CORRECT for x in range(0, 5)])

    letter_scores = []
    for (guess_letter, correct_letter) in zip(guess, solution):
        if guess_letter == correct_letter:
            letter_scores.append(CORRECT)
        elif guess_letter in solution:
            letter_scores.append(MISPLACED)
        else:
            letter_scores.append(WRONG)

    return (False, letter_scores)


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
        "max_guesses": args.exploration,
        "max_known_letters": 4
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
