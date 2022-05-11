import logging
import wordle_dict as wd
import log_config  # import does logging config
import wordle_strategy as ws
import presorted_list_word_scorer as plws

log = logging.getLogger(__name__)


class LaxMellorStrategy:
    '''Attempts to solve the puzzle using the strategy described by Myles Mellor in this article:
        https://www.9news.com/article/news/local/zevely-zone/five-magic-words-that-will-solve-wordle/509-fec2b387-5202-4d74-8c47-fde9221a82c1#l30tu0p44eve1xn6njh

        After using the five words chosen by Mellor, uses the standard CombinedWordScoreStrategy for the last word'''

    def __init__(self):
        self.forced_words = ['derby', 'flank', 'ghost', 'winch', 'jumps']
        self.inner_strategy = ws.WordleStrategy(lambda: plws.PresortedListWordScorer(
            wd.load_combined_word_score_dictionary()), {"max_guesses": 3, "first_word": ""})

    def next_guess(self):
        if self.forced_words:
            return self.forced_words.pop(0)
        else:
            return self.inner_strategy.next_guess()

    def accept_result(self, results: list[str], guess: str):
        log.debug(f"accept_result, word={guess}, result={results}")

        self.inner_strategy.accept_result(results, guess)
