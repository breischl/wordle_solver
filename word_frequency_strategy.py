import wordle_dict as wd
from collections import Counter
import logging
import log_config  # import does logging config
from wordle_util import WRONG, CORRECT, MISPLACED
import wordle_util as wu

log = logging.getLogger(__name__)


class WordFrequencyStrategy:
    def __init__(self, dictionary: list[tuple[str, int]] = wd.load_frequency()):
        self.dictionary = dictionary

    def next_guess(self):
        guess = self.dictionary[0][0] if self.dictionary else None
        log.debug(f"next_guess={guess}")
        return guess

    def accept_result(self, results: list[str], guess: str):
        log.debug(f"accept_result, word={guess}, result={results}")

        repeated_letter_counts = wu.count_repeats_in_solution(guess, results)

        guess_letter_counts = Counter(guess)

        log.debug("Repeated letters: %s", repeated_letter_counts)

        new_dictionary = []
        for ws_tuple in self.dictionary:
            if wu.is_possible_solution(ws_tuple[0], guess, results, guess_letter_counts, repeated_letter_counts):
                new_dictionary.append(ws_tuple)

        self.dictionary = new_dictionary
