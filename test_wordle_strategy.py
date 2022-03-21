import unittest
import wordle_strategy as ws
import wordle_dict as wd
from wordle_util import WRONG, MISPLACED, CORRECT


class TestWordleStrategy(unittest.TestCase):
    def setUp(self) -> None:
        self.strat = ws.WordleStrategy(wd.load_dictionary())
        return super().setUp()

    def test_accepts_feedback(self):
        initial_size = len(self.strat.precision_word_scorer.wordlist)
        self.strat.accept_result(
            [WRONG, WRONG, MISPLACED, CORRECT, CORRECT], "arose")
        new_size = len(self.strat.precision_word_scorer.wordlist)
        self.assertLess(new_size, initial_size)
