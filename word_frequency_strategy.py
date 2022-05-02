import wordle_dict as wd
import logging
import log_config  # import does logging config
import wordle_util as wu

log = logging.getLogger(__name__)


class WordFrequencyStrategy:
    def __init__(self, dictionary: list[tuple[str, int]] = wd.load_frequency(), exploration_settings: map = None):
        self.dictionary = dictionary

        exploration_settings = exploration_settings or {"first_word": "raise"}

        # This is what Dave was using, so for now we're matching that to validate parity with his implementation
        self.forced_first_word = exploration_settings["first_word"]

    def next_guess(self):
        if self.forced_first_word:
            guess = self.forced_first_word
            self.forced_first_word = None
        else:
            guess = self.dictionary[0][0] if self.dictionary else None

        log.debug(f"next_guess={guess}")
        return guess

    def accept_result(self, results: list[str], guess: str):
        log.debug(f"accept_result, word={guess}, result={results}")

        misplaced_letters = wu.count_misplaced_letters(guess, results)

        log.debug("Misplaced letters: %s", misplaced_letters)

        new_dictionary = []
        for ws_tuple in self.dictionary:
            if wu.is_possible_solution(ws_tuple[0], guess, results, misplaced_letters):
                new_dictionary.append(ws_tuple)

        if len(new_dictionary) == len(self.dictionary):
            log.warn(
                f"Feedback didn't remove any words from consideration. old_size={len(self.dictionary)}, new_size={len(new_dictionary)}")

        self.dictionary = new_dictionary
