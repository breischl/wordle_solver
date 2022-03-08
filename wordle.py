import random
import stats
from wordle_dict import *

WRONG = -1
MISPLACED = 0
CORRECT = 1


def check_word(solution: str, guess: str) -> tuple:
    '''Check whether a given guess matches the expected solution, and return that along with match scores for each letter. 


    Returns: (is_correct : bool, letter_scores : list[int])
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


def is_possible_solution(word: str, guess: str, letter_scores: list) -> bool:
    '''Check if a given word could possibly be the solution, given the results of a previous guess.
    '''
    for idx in range(0, len(guess)):
        l_word = word[idx]
        l_guess = guess[idx]
        score = letter_scores[idx]
        # print("{0}, guess={1}, score={2}, word={3}".format(
        #     idx, l_guess, score, l_word))

        if score == CORRECT and l_word != l_guess:
            # print("Guess was correct, word is not, result False")
            return False
        elif score == MISPLACED and l_word == l_guess:
            # print("Guess was misplaced, word has letter in same position, result False")
            return False
        elif score == MISPLACED and l_guess not in word:
            # print("Guess was misplaced, word doesn't have that letter anywhere, result False")
            return False
        elif score == WRONG and l_guess in word:
            # print("Guess was wrong, word contains that letter, result False")
            return False

    return True


if __name__ == "__main__":
    words = load_dictionary()
    solution = random.choice(words)
    print(f"Solution is '{solution}'")

    for guess_num in range(1, 7):
        print(f"\nI can think of {len(words)} possible words")

        allow_dup = (guess_num > 3)
        best_guesses = stats.find_highest_scoring_words(words, allow_dup)

        print(f"Best words are {best_guesses}, I'll use the first one")
        guess_word = best_guesses[0][0]
        (is_correct, letter_scores) = check_word(solution, guess_word)

        if is_correct:
            print(f"'{guess_word}' is correct, I win!")
            break

        print(f"'{guess_word}' was wrong, letter scores are: {letter_scores}")
        words = [w for w in words if is_possible_solution(
            w, guess_word, letter_scores)]
