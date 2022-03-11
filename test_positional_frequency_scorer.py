import unittest
import positional_frequency_scorer as pfs
import wordle_dict as wd
from wordle_strategy import WRONG
from wordle_strategy import MISPLACED
from wordle_strategy import CORRECT


class TestPositionalFrequencyScorer(unittest.TestCase):
    def setUp(self) -> None:
        self.scorer = pfs.PositionalFrequencyWordScorer()
        self.words = wd.load_dictionary()

    def test_first_guess_works(self):
        guess = self.scorer._choose_next_word(self.words, False)
        self.assertEqual(guess, "cares")

    def test_find_highest_scoring_single_word(self):
        the_best_words = self.scorer._find_highest_scoring_words([
                                                                 "sweet"], True)
        self.assertEqual(len(the_best_words[0]), 1, "List should be non-empty")
        self.assertEqual(the_best_words[0][0], "sweet")
