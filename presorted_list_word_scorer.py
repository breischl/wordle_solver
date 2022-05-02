import logging
import log_config
import wordle_util as wu

log = logging.getLogger(__name__)


class PresortedListWordScorer:
    '''A word scorer that assumes the list it's given is in preference order, and just returns the first matching word'''

    def __init__(self, wordlist: list[str]):
        self.wordlist = wordlist

    def _choose_next_word(self, allow_double_letters: bool) -> str:
        if self.wordlist:
            return self.wordlist[0]
        else:
            None

    def remove_non_matching_words(self, guess: str, letter_scores: list[str]) -> None:
        (new_wordlist, removed_words) = wu.remove_non_matching_words(
            self.wordlist, guess, letter_scores)

        self.wordlist = new_wordlist

    def remove_words_containing_letters(self, letters: str) -> None:
        (new_wordlist, removed_words) = wu.remove_words_containing_letters(
            self.wordlist, letters)

        self.wordlist = new_wordlist
