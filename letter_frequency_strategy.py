from positional_frequency_scorer import PositionalFrequencyWordScorer
import wordle_dict as wd
import logging
import log_config  # import does logging config
from wordle_util import WRONG, CORRECT, MISPLACED

log = logging.getLogger(__name__)


class WordleLetterFrequencyStrategy:
    '''A Wordle guessing strategy.
    '''

    def __init__(self, dictionary: list[str] = wd.load_dictionary(), exploration_settings: map = None):
        self.precision_word_scorer = PositionalFrequencyWordScorer(
            dictionary.copy())
        self.guess_num = 1

        exploration_settings = exploration_settings or default_exploration_settings()
        self.max_exploration_guesses = exploration_settings["max_guesses"]

        if self.max_exploration_guesses > 0:
            self.exploration_mode = True
            self.exploration_word_scorer = PositionalFrequencyWordScorer(
                dictionary.copy())
        else:
            self.exploration_mode = False
            self.exploration_word_scorer = None

    def next_guess(self):
        log.debug(
            f"next_guess, guess={self.guess_num}, exploration_mode={self.exploration_mode}")

        guess = None
        if self.exploration_mode:
            guess = self.exploration_word_scorer._choose_next_word(
                False)

        if guess is None:
            guess = self.precision_word_scorer._choose_next_word(True)

        log.debug(f"next_guess={guess}")
        return guess

    def accept_result(self, results: list[str], guess: str):
        log.debug(f"accept_result, word={guess}, result={results}")

        self.precision_word_scorer.remove_non_matching_words(guess, results)

        if(self.exploration_word_scorer):
            self.exploration_word_scorer.remove_words_containing_letters(guess)

        if self.exploration_mode and not self._should_explore():
            log.debug("Exiting exploration mode")
            self._stop_exploring()

        self.guess_num += 1

    def _should_explore(self) -> bool:
        log.debug(
            f"_should_explore, guess_num={self.guess_num}, max_guesses={self.max_exploration_guesses}, "
            f"exploration_dict_len={len(self.exploration_word_scorer.wordlist)}")
        return bool(self.guess_num <= self.max_exploration_guesses
                    and self.exploration_word_scorer)

    def _stop_exploring(self):
        self.exploration_mode = False
        self.exploration_word_scorer = None


def default_exploration_settings() -> map:
    return {
        "max_guesses": 4
    }
