import wordle_dict as wd

WRONG = "w"
MISPLACED = "m"
CORRECT = "c"


class WordleStrategy:
    '''A base class for Wordle guessing strategies. This class handles tracking the dictionary, guess number, guesses and some options. 

        In particular the constructor arguments `allow_dup_letters_after_guess`, which disallows early guessing of words that contain the same letter more than once. 
        Also `allow_letter_repetition_after_guess`, which will force guessing new letters early on, even if some letters were correct. It basically treats "correct" letters like "wrong" letters, until later guesses. 
    '''

    def __init__(self, dictionary: list[str] = wd.load_dictionary(), allow_dup_letters_after_guess: int = 2, allow_letter_repetition_after_guess: int = 0):
        self.words = dictionary
        self.allow_dup_letters_after_guess = allow_dup_letters_after_guess
        self.allow_letter_repetition_after_guess = allow_letter_repetition_after_guess
        self.last_guess = None
        self.guess_num = 1

        if allow_letter_repetition_after_guess > 0:
            self.shadow_dictionary = self.words.copy()
        else:
            self.shadow_dictionary = []

    def next_guess(self):
        if len(self.shadow_dictionary) == 1:
            next_guess = self.shadow_dictionary[0]
        elif not self.shadow_dictionary and len(self.words) == 1:
            next_guess = self.words[0]
        else:
            next_guess = self._choose_next_word(
                self._duplicate_letters_allowed())
            if next_guess is None and self.shadow_dictionary:
                self.words = self.shadow_dictionary
                self.shadow_dictionary = []
                next_guess = self.next_guess()

        self.last_guess = next_guess
        return next_guess

    def accept_result(self, results: list[str], guess: str = None):
        guess = guess or self.last_guess

        if self.guess_num < self.allow_letter_repetition_after_guess:
            self.shadow_dictionary = remove_non_matching_words(
                self.shadow_dictionary, guess, results)
            self.words = remove_non_matching_words(
                self.words, guess, list("wwwww"))
        elif self.guess_num >= self.allow_letter_repetition_after_guess:
            if self.shadow_dictionary:
                self.words = self.shadow_dictionary
                self.shadow_dictionary = []
            self.words = remove_non_matching_words(self.words, guess, results)

        self.guess_num += 1

    def _duplicate_letters_allowed(self):
        return self.guess_num > self.allow_dup_letters_after_guess

    def _choose_next_word(self, allow_dup_letters: bool) -> str:
        return self.words[0]  # implementers should override


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


def remove_non_matching_words(wordlist: list[str], guess: str, letter_scores: list[str]) -> list[str]:
    return [w for w in wordlist if is_possible_solution(w, guess, letter_scores)]
