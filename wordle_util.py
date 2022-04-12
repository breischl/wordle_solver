from collections import defaultdict
from collections import Counter
from timeit import repeat
import log_config
import logging

WRONG = "w"
MISPLACED = "m"
CORRECT = "c"

log = logging.getLogger(__name__)


def check_word(solution: str, guess: str) -> tuple[bool, list[str]]:
    '''Check whether a given guess matches the expected solution, and return that along with match scores for each letter.

    Returns: (is_correct : bool, letter_scores : list[str])
    '''
    if solution == guess:
        return (True, [CORRECT for x in range(0, 5)])

    solution_letters = list(solution)
    guess_letters = list(guess)
    letter_scores = [None for x in range(0, 5)]

    for (idx, (guess_letter, correct_letter)) in enumerate(zip(guess_letters, solution_letters)):
        if guess_letter == correct_letter:
            letter_scores[idx] = CORRECT
            solution_letters[idx] = None
            guess_letters[idx] = None

    for (idx, guess_letter) in enumerate(guess_letters):
        if guess_letter is None:
            continue
        elif guess_letter in solution_letters:
            letter_scores[idx] = MISPLACED
            solution_letters.remove(guess_letter)
        else:
            letter_scores[idx] = WRONG

    return (False, letter_scores)


def count_repeats_in_solution(guess: str, letter_scores: list[str]) -> dict[str, int]:
    '''Count the number of times a letter got a non-WRONG answer in the result. This is the number of times we expect the letter in the solution.
    '''
    repeated_letter_counts = defaultdict(int)
    for (guess_letter, score) in zip(guess, letter_scores):
        if score != WRONG:
            repeated_letter_counts[guess_letter] += 1

    for letter in list(repeated_letter_counts.keys()):
        if repeated_letter_counts[letter] < 2:
            del repeated_letter_counts[letter]

    return repeated_letter_counts


def is_possible_solution(word: str, guess: str, letter_scores: list, guess_letter_counts: Counter, repeated_letter_counts: dict[str, int]) -> bool:
    '''Check if a given word could possibly be the solution, given the results of a previous guess.

    `repeated_letter_counts` can be obtained from the `count_repeats_in_solution()` function.

    '''
    for (l_word, l_guess, score) in zip(word, guess, letter_scores):
        if score == CORRECT and l_word != l_guess:
            # log.debug(
            #     "Letter was correct, word doesn't have it at that position, result False")
            return False
        elif score == MISPLACED and l_word == l_guess:
            # log.debug(
            #     "Letter was misplaced, word has letter in same position, result False")
            return False
        elif score == MISPLACED and l_guess not in word:
            # log.debug(
            #     "Letter was misplaced, word doesn't have that letter anywhere, result False")
            return False
        elif score == WRONG and l_guess in word and l_guess not in repeated_letter_counts and guess_letter_counts[l_guess] == 1:
            # log.debug(
            #     "Letter was wrong and it wasn't repeated, word contains that letter, result False")
            return False

    if repeated_letter_counts:
        for (letter, count) in repeated_letter_counts.items():
            if word.count(letter) < count:
                log.debug("Expected letter to be repeated, but it wasn't")
                return False

    return True


def remove_non_matching_words(wordlist: list[str], guess: str, letter_scores: list[str]) -> tuple[list[str], list[str]]:
    new_wordlist = []
    words_removed = []

    repeated_letter_counts = count_repeats_in_solution(
        guess, letter_scores)

    guess_letter_counts = Counter(guess)

    log.debug("Repeated letters: %s", repeated_letter_counts)

    for word in wordlist:
        if is_possible_solution(word, guess, letter_scores, guess_letter_counts, repeated_letter_counts):
            new_wordlist.append(word)
        else:
            words_removed.append(word)

    return (new_wordlist, words_removed)


def remove_words_containing_letters(wordlist: list[str], letters: str) -> tuple[list[str], list[str]]:
    letter_set = set(letters)
    new_wordlist = []
    words_removed = []

    for word in wordlist:
        if letter_set.isdisjoint(word):
            new_wordlist.append(word)
        else:
            words_removed.append(word)

    return (new_wordlist, words_removed)
