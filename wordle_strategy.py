from argparse import Namespace
import wordle_dict as wd
import log_config
import logging


WRONG = "w"
MISPLACED = "m"
CORRECT = "c"

log = logging.getLogger(__name__)


class WordleStrategy:
    '''A base class for Wordle guessing strategies. This class handles tracking the dictionary, guess number, guesses and some options. 

        In particular the constructor arguments `allow_dup_letters_after_guess`, which disallows early guessing of words that contain the same letter more than once. 
        Also `allow_letter_repetition_after_guess`, which will force guessing new letters early on, even if some letters were correct. It basically treats "correct" letters like "wrong" letters, until later guesses. 
    '''

    def __init__(self, word_scorer, dictionary: list[str] = wd.load_dictionary(), exploration_settings: map = None):
        self.word_scorer = word_scorer
        self.last_guess = None
        self.guess_num = 1
        self.exploration_mode = True

        exploration_settings = exploration_settings or default_exploration_settings()
        self.max_exploration_guesses = exploration_settings["max_guesses"]

        self.precision_dictionary = dictionary

        if self.max_exploration_guesses > 1:
            self.exploration_dictionary = dictionary.copy()
        else:
            self.exploration_dictionary = []

    def next_guess(self):
        log.debug(
            f"next_guess, guess={self.guess_num}, exploration_mode={self.exploration_mode}")

        if self.exploration_mode:
            self.last_guess = self.word_scorer._choose_next_word(
                self.exploration_dictionary, False)
        else:
            self.last_guess = self.word_scorer._choose_next_word(
                self.precision_dictionary, (self.guess_num < 6))

        # last guess failed, so we're out of words without duplicate letters. So start checking words with duplicates
        if self.last_guess is None:
            self.last_guess = self.word_scorer._choose_next_word(
                self.precision_dictionary, True)

        log.debug(f"next_guess={self.last_guess}")
        return self.last_guess

    def accept_result(self, results: list[str], guess: str = None):
        guess = guess or self.last_guess

        log.debug(f"accept_result, word={guess}, result={results}")

        self.precision_dictionary = remove_non_matching_words(
            self.precision_dictionary, guess, results)
        self.exploration_dictionary = remove_words_containing_letters(
            self.exploration_dictionary, guess)

        if self.exploration_mode and not self._should_explore():
            log.debug("Exiting exploration mode")
            self._stop_exploring()

        self.guess_num += 1

    def _should_explore(self) -> bool:
        log.debug(
            f"_should_explore, guess_num={self.guess_num}, max_guesses={self.max_exploration_guesses}, "
            f"exploration_dict_len={len(self.exploration_dictionary)}")
        return bool(self.guess_num <= self.max_exploration_guesses
                    and self.exploration_dictionary)

    def _stop_exploring(self):
        self.exploration_mode = False
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


def default_exploration_settings() -> map:
    return {
        "max_guesses": 4
    }


def remove_non_matching_words(wordlist: list[str], guess: str, letter_scores: list[str]) -> list[str]:
    return [w for w in wordlist if is_possible_solution(w, guess, letter_scores)]


def remove_words_containing_letters(wordlist: list[str], letters: str) -> list[str]:
    letter_set = set(letters)
    return [w for w in wordlist if letter_set.isdisjoint(w)]
