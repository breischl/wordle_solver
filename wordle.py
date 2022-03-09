'''Functions for manipulating the in-memory dictionary and checking word results
'''
import random
from wordle_dict import *
import positional_frequency_strategy as pfs
import global_frequency_strategy as gfs
import argparse as arg
from wordle_strategy import WRONG
from wordle_strategy import MISPLACED
from wordle_strategy import CORRECT


def check_word(solution: str, guess: str) -> tuple[bool, list[str]]:
    '''Check whether a given guess matches the expected solution, and return that along with match scores for each letter. 


    Returns: (is_correct : bool, letter_scores : list[str])
    '''
    if solution == guess:
        return (True, [CORRECT for x in range(0, 5)])

    letter_scores = []
    for idx in range(0, len(guess)):
        guess_letter = guess[idx]
        correct_letter = solution[idx]
        if guess_letter == correct_letter:
            letter_scores.append(CORRECT)
        elif guess_letter in solution:
            letter_scores.append(MISPLACED)
        else:
            letter_scores.append(WRONG)

    return (False, letter_scores)


if __name__ == "__main__":
    parser = arg.ArgumentParser(
        description="Computer plays a game of Wordle against itself")
    parser.add_argument("-s", "--solution", type=str,
                        help="Optionally specify the solution word for the computer to guess")
    parser.add_argument("--strategy", type=str, default="PositionalFrequency",
                        choices=["PositionalFrequency", "GlobalFrequency"])
    parser.add_argument("-d", "--duplicates", default=3, type=int,
                        help="Number of guesses before suggesting words containing the same letter more than once")
    parser.add_argument("-r", "--repetition", default=3, type=int,
                        help="Number of guesses before suggesting words containing previously-guessed letters. ie, all letters suggested will be new until this many guesses.")
    args = parser.parse_args()

    words = load_dictionary()
    solution = args.solution or random.choice(words)

    if(args.strategy == "PositionalFrequency"):
        strat = pfs.PositionalFrequencyStrategy(
            dictionary=words, allow_dup_letters_after_guess=args.duplicates, allow_letter_repetition_after_guess=args.repetition)
    elif(args.strategy == "GlobalFrequency"):
        strat = gfs.GlobalFrequencyStrategy(
            dictionary=words, allow_dup_letters_after_guess=args.duplicates, allow_letter_repetition_after_guess=args.repetition)
    else:
        print(f"Unknown strategy: {args.strategy}")
        quit()

    print(f"Solution is '{solution}'")

    for guess_num in range(1, 7):
        guess_word = strat.next_guess()
        print(f"I'll guess '{guess_word}'")

        (is_correct, letter_scores) = check_word(solution, guess_word)

        if is_correct:
            print(f"'{guess_word}' is correct, I win!")
            break

        letter_score_str = str.join("", letter_scores)
        print(f"'{guess_word}' was wrong, letter scores are: {letter_score_str}")

        strat.accept_result(letter_scores)
