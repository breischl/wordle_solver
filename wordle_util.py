WRONG = "w"
MISPLACED = "m"
CORRECT = "c"


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


def is_possible_solution(word: str, guess: str, letter_scores: list) -> bool:
    '''Check if a given word could possibly be the solution, given the results of a previous guess.
    '''
    for (l_word, l_guess, score) in zip(word, guess, letter_scores):
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
