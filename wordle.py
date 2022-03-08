import random

WRONG = -1
MISPLACED = 0
CORRECT = 1
DICTIONARY_FILE = 'words_alpha.txt'


def load_dictionary() -> list:
    '''Load and return the dictionary as a list[str]
    Returns: list[str]
    '''
    with open(DICTIONARY_FILE, mode="rt") as word_file:
        valid_words = [w for w in word_file.read().splitlines()]
    return valid_words


def cleanse_dictionary() -> None:
    '''Read in the dictionary file, remove invalid words, and write the result back'''
    with open(DICTIONARY_FILE, mode="rt") as word_file:
        valid_words = [w
                       for w in word_file.read().splitlines()
                       if is_valid_word(w)]

    save_dictionary(valid_words)


def save_dictionary(words: list) -> None:
    '''Save the given list to the dictionary file
    '''

    with open(DICTIONARY_FILE, mode="wt") as word_file:
        for w in words:
            word_file.write(w)
            word_file.write("\n")


def is_valid_word(w: str):
    '''Filter invalid words from the dictionary
    '''
    return len(w) == 5 and w.isalpha()


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
    print("Solution is '{0}'".format(solution))

    for guess_num in range(1, 7):
        print("Dictionary contains {0} words".format(len(words)))

        guess_word = random.choice(words)
        print("For guess {0} I'll try '{1}'".format(guess_num, guess_word))
        (is_correct, letter_scores) = check_word(solution, guess_word)

        if is_correct:
            print("{0} is correct, I win!".format(guess_word))
            break

        print("{0} was wrong, results by letter are {1}".format(
            guess_word, letter_scores))
        words = [w for w in words if is_possible_solution(
            w, guess_word, letter_scores)]
