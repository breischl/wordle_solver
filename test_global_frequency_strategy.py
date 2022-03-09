import unittest
import global_frequency_strategy as gfs
import wordle_dict as wd
from wordle import WRONG
from wordle import MISPLACED
from wordle import CORRECT


class TestGlobalFrequencyStrategy(unittest.TestCase):
    def setUp(self) -> None:
        self.strat = gfs.GlobalFrequencyStrategy(wd.load_dictionary())

    def test_first_guess_works(self):
        guess = self.strat.next_guess()
        self.assertEqual(guess, "arose")

    def test_accepts_feedback(self):
        initial_size = len(self.strat.words)
        self.strat.accept_result(
            [WRONG, WRONG, MISPLACED, CORRECT, CORRECT], "arose")
        new_size = len(self.strat.words)
        self.assertLess(new_size, initial_size)

    def test_find_highest_scoring_no_dups_excludes_all_answers(self):
        self.strat = gfs.GlobalFrequencyStrategy(dictionary=["sweet"])
        the_best_words = self.strat._find_highest_scoring_words(False)
        self.assertEqual(len(the_best_words[0]), 1,
                         F"List should be non-empty but was: {the_best_words}")
        self.assertEqual(the_best_words[0][0], "sweet")

    def test_find_highest_scoring_with_dups(self):
        self.strat = gfs.GlobalFrequencyStrategy(dictionary=["sweet"])
        the_best_words = self.strat._find_highest_scoring_words(True)
        self.assertEqual(len(the_best_words[0]), 1, "List should be non-empty")
        self.assertEqual(the_best_words[0][0], "sweet")
