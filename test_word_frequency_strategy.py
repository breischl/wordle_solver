import unittest
import word_frequency_strategy as ws
import wordle_dict as wd
from wordle_util import WRONG, MISPLACED, CORRECT


class TestWordleStrategy(unittest.TestCase):
    def setUp(self) -> None:
        self.strat = ws.WordFrequencyStrategy()
        return super().setUp()

    def test_basic_function(self) -> None:
        forced_word = self.strat.forced_first_word
        guess = self.strat.next_guess()
        self.assertEqual(guess, forced_word)

        self.strat.accept_result(
            [WRONG, WRONG, MISPLACED, WRONG, MISPLACED], guess)
        guess = self.strat.next_guess()
        self.assertEqual("video", guess)
