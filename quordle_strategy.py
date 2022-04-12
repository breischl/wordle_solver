from positional_frequency_scorer import PositionalFrequencyWordScorer
import wordle_dict as wd
import logging
import log_config  # import does logging config
from wordle_util import WRONG, CORRECT, MISPLACED

log = logging.getLogger(__name__)


class QuordleStrategy:
    '''A Quordle guessing strategy.
    '''

    def __init__(self, dictionary: list[str] = wd.load_dictionary(), exploration_settings: map = None):
        self.precision_word_scorers = [PositionalFrequencyWordScorer(
            dictionary.copy()) for x in range(0, 4)]
        self.correct_words = [None, None, None, None]
        self.guess_num = 1
        self.exploration_mode = True

        exploration_settings = exploration_settings or default_exploration_settings()
        self.max_exploration_guesses = exploration_settings["max_guesses"]

        if self.max_exploration_guesses > 1:
            self.exploration_word_scorer = PositionalFrequencyWordScorer(
                dictionary.copy())
        else:
            self.exploration_word_scorer = None

    def next_guess(self):
        log.debug(
            f"next_guess, guess={self.guess_num}, exploration_mode={self.exploration_mode}")

        guess = None
        if self.exploration_mode:
            guess = self.exploration_word_scorer._choose_next_word(
                False)
        else:
            guess = self._choose_best_precision_scorer(
            )._choose_next_word(self.guess_num < 6)

        # last guess failed, so we're out of words without duplicate letters. So start checking words with duplicates
        if guess is None:
            guess = self._choose_best_precision_scorer()._choose_next_word(True)

        if guess is None:
            log.debug(f"Failed to come up with a guess!")
            return None

        log.debug(f"next_guess={guess}")
        return guess

    def _choose_best_precision_scorer(self):
        log.debug("Choosing best precision scorer...")
        return min(self.precision_word_scorers,
                   key=lambda s: 99999 if s is None else len(s.wordlist))

    def accept_results(self, results: list[list[str]], guess: str):
        log.debug(f"accept_result, word={guess}, result={results}")

        # Update each individual scorer with its own result
        for (idx, (scorer, single_result)) in enumerate(zip(self.precision_word_scorers, results)):
            if scorer is None or single_result is None:
                # we already won this one
                log.debug(f"Already won for scorer {idx}")
                continue
            elif single_result == list("ccccc"):
                # we won!
                # Remove this scorer from consideration
                log.debug(f"Won puzzle for scorer {idx}")
                self.precision_word_scorers[idx] = None
            else:
                log.debug(
                    f"Removing non-matching words for scorer {idx}, guess={guess}, result={single_result}")
                scorer.remove_non_matching_words(guess, single_result)

        for (idx, scorer) in enumerate(self.precision_word_scorers):
            word_count = None if scorer is None else len(scorer.wordlist)
            log.debug(f"Scorer {idx}, len(wordlist)={word_count}")

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
                    and self.exploration_word_scorer
                    and len(self.exploration_word_scorer.wordlist) > 0)

    def _stop_exploring(self):
        self.exploration_mode = False
        self.exploration_word_scorer = None


def default_exploration_settings() -> map:
    return {
        "max_guesses": 4
    }
