import unittest
import wordle_strategy as ws
import wordle_dict as wd
import presorted_list_word_scorer as psl
from wordle_util import WRONG, MISPLACED, CORRECT


class TestWordleStrategy(unittest.TestCase):
    def setUp(self) -> None:
        words = wd.load_combined_word_score_dictionary()
        self.strat = ws.WordleStrategy(
            lambda: psl.PresortedListWordScorer(words.copy()))
        return super().setUp()

    def test_accepts_feedback(self):
        initial_size = len(self.strat.precision_word_scorer.wordlist)
        self.assertEqual("about", self.strat.next_guess())
        self.strat.accept_result(
            [WRONG, WRONG, MISPLACED, CORRECT, CORRECT], "about")
        new_size = len(self.strat.precision_word_scorer.wordlist)
        self.assertLess(new_size, initial_size)
