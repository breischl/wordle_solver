import unittest
import positional_frequency_scorer as pfs
import wordle_dict as wd
from wordle_strategy import WRONG
from wordle_strategy import MISPLACED
from wordle_strategy import CORRECT


class TestPositionalFrequencyScorer(unittest.TestCase):
    def setUp(self) -> None:
        self.words = wd.load_dictionary()
        self.scorer = pfs.PositionalFrequencyWordScorer(self.words)

    def test_first_guess_works(self):
        guess = self.scorer._choose_next_word(False)
        self.assertEqual(guess, "cares")

    def test_find_highest_scoring_single_word(self):
        self.words.clear()
        self.words.append("sweet")
        the_best_words = self.scorer._find_highest_scoring_words(True)
        self.assertEqual(len(the_best_words[0]), 1, "List should be non-empty")
        self.assertEqual(the_best_words[0][0], "sweet")

    def test_remove_non_matching_words(self):
        initial_size = len(self.scorer.wordlist)
        initial_2_o_frequency = self.scorer.position_counts[2]["o"]
        self.scorer.remove_non_matching_words(
            "arose", [WRONG, WRONG, MISPLACED, CORRECT, CORRECT])

        self.assertLess(len(self.scorer.wordlist), initial_size)
        self.assertEqual(self.scorer.position_counts[0]["a"], 0)
        self.assertEqual(self.scorer.position_counts[1]["r"], 0)
        self.assertEqual(self.scorer.position_counts[2]["o"], 0)
        self.assertEqual(self.scorer.position_counts[3]["a"], 0)
        self.assertEqual(self.scorer.position_counts[3]["b"], 0)
        self.assertEqual(self.scorer.position_counts[3]["c"], 0)

    def test_remove_words_containing_letters(self):
        initial_size = len(self.scorer.wordlist)
        initial_2_o_frequency = self.scorer.position_counts[2]["o"]
        self.scorer.remove_words_containing_letters("arose")

        self.assertLess(len(self.scorer.wordlist), initial_size)
        for pos_counts in self.scorer.position_counts:
            self.assertEqual(0, pos_counts["a"])
            self.assertEqual(0, pos_counts["r"])
            self.assertEqual(0, pos_counts["o"])
            self.assertEqual(0, pos_counts["s"])
            self.assertEqual(0, pos_counts["e"])
