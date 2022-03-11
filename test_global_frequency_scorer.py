import unittest
import global_frequency_scorer as gfs
import wordle_dict as wd
from wordle_strategy import WRONG
from wordle_strategy import MISPLACED
from wordle_strategy import CORRECT


class TestGlobalFrequencyScorer(unittest.TestCase):
    def setUp(self) -> None:
        self.scorer = gfs.GlobalFrequencyWordScorer()
        self.words = wd.load_dictionary()

    def test_first_guess_works(self):
        guess = self.scorer._choose_next_word(self.words, False)
        self.assertEqual(guess, "aeros")

    def test_find_highest_scoring_no_dups_excludes_all_answers(self):
        the_best_words = self.scorer._find_highest_scoring_words([
            "sweet"], True)
        self.assertEqual(len(the_best_words[0]), 1,
                         F"List should be non-empty but was: {the_best_words}")
        self.assertEqual(the_best_words[0][0], "sweet")
