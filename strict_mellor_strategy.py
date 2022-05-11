import logging
import wordle_dict as wd
import log_config  # import does logging config
import wordle_strategy as ws
import presorted_list_word_scorer as plws
import wordle_util as wu

log = logging.getLogger(__name__)


class StrictMellorStrategy:
    '''Attempts to solve the puzzle using the strategy described by Myles Mellor in this article:
        https://www.9news.com/article/news/local/zevely-zone/five-magic-words-that-will-solve-wordle/509-fec2b387-5202-4d74-8c47-fde9221a82c1#l30tu0p44eve1xn6njh

        After using the five words chosen by Mellor, if there is more than one possible word remaining returns None'''

    def __init__(self, wordlist: list[str]):
        self.forced_words = ['derby', 'flank', 'ghost', 'winch', 'jumps']
        self.wordlist = wordlist

    def next_guess(self):
        if self.forced_words:
            return self.forced_words.pop(0)
        elif len(self.wordlist) == 1:
            return self.wordlist[0]
        else:
            log.debug("More than one possible word remains: %s",
                      str.join(", ", self.wordlist))
            return None

    def accept_result(self, results: list[str], guess: str):
        log.debug(f"accept_result, word={guess}, result={results}")

        (new_wordlist, _) = wu.remove_non_matching_words(
            self.wordlist, guess, results)
        self.wordlist = new_wordlist
