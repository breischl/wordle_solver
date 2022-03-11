from argparse import Namespace
import wordle_dict as wd

WRONG = "w"
MISPLACED = "m"
CORRECT = "c"


class WordleStrategy:
    '''A base class for Wordle guessing strategies. This class handles tracking the dictionary, guess number, guesses and some options. 

        In particular the constructor arguments `allow_dup_letters_after_guess`, which disallows early guessing of words that contain the same letter more than once. 
        Also `allow_letter_repetition_after_guess`, which will force guessing new letters early on, even if some letters were correct. It basically treats "correct" letters like "wrong" letters, until later guesses. 
    '''

    def __init__(self, word_scorer, dictionary: list[str] = wd.load_dictionary(), exploration_settings: map = None):
        self.word_scorer = word_scorer
        self.last_guess = None
        self.guess_num = 1
        # Letters that we know are in the word somewhere, ie we got a "misplaced" or "correct" on them
        self.known_letters = set()

        exploration_settings = exploration_settings or default_settings()
        self.max_exploration_guesses = exploration_settings["max_exploration_guesses"]

        self.precision_dictionary = dictionary

        if self.max_exploration_guesses > 1:
            self.exploration_dictionary = dictionary.copy()
        else:
            self.exploration_dictionary = []

    def next_guess(self):
        if self._should_explore():
            self.last_guess = self.word_scorer._choose_next_word(
                self.exploration_dictionary, False)
        else:
            self.last_guess = self.word_scorer._choose_next_word(
                self.precision_dictionary, True)

        return self.last_guess

    def accept_result(self, results: list[str], guess: str = None):
        guess = guess or self.last_guess

        for (letter, result) in zip(guess, results):
            if result == CORRECT or result == MISPLACED:
                self.known_letters.add(letter)

        self.precision_dictionary = remove_non_matching_words(
            self.precision_dictionary, guess, results)
        self.exploration_dictionary = remove_words_containing_letters(
            self.exploration_dictionary, guess)

        if not self._should_explore():
            self._stop_exploring()

        self.guess_num += 1

    def _should_explore(self):
        return self.guess_num <= self.max_exploration_guesses \
            and self.exploration_dictionary \
            and len(self.known_letters) < 4

    def _stop_exploring(self):
        self.exploration_dictionary = []


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


def default_settings() -> map:
    return {
        "max_exploration_guesses": 4,
        "guess_words_multiplier": 4,
    }


def remove_non_matching_words(wordlist: list[str], guess: str, letter_scores: list[str]) -> list[str]:
    return [w for w in wordlist if is_possible_solution(w, guess, letter_scores)]


def remove_words_containing_letters(wordlist: list[str], letters: str) -> list[str]:
    letter_set = set(letters)
    return [w for w in wordlist if letter_set.isdisjoint(w)]
