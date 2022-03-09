'''Functions for manipulating the in-memory dictionary and checking word results
'''
import random
from wordle_dict import *
import positional_frequency_strategy as pfs
import global_frequency_strategy as gfs
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
    words = load_dictionary()
    solution = random.choice(words)
    # strat = pfs.PositionalFrequencyStrategy(words)
    strat = gfs.GlobalFrequencyStrategy(words)

    print(f"Solution is '{solution}'")

    for guess_num in range(1, 7):
        print(f"\nI can think of {len(strat.words)} possible words")

        guess_word = strat.next_guess()
        print(f"I'll guess '{guess_word}'")

        (is_correct, letter_scores) = check_word(solution, guess_word)

        if is_correct:
            print(f"'{guess_word}' is correct, I win!")
            break

        letter_score_str = str.join("", letter_scores)
        print(f"'{guess_word}' was wrong, letter scores are: {letter_score_str}")

        strat.accept_result(letter_scores)
