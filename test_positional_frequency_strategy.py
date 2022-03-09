import unittest
import positional_frequency_strategy as pfs
import wordle_dict as wd
from wordle_strategy import WRONG
from wordle_strategy import MISPLACED
from wordle_strategy import CORRECT


class TestPositionalFrequencyStrategy(unittest.TestCase):
    def setUp(self) -> None:
        self.strat = pfs.PositionalFrequencyStrategy(wd.load_dictionary())

    def test_first_guess_works(self):
        guess = self.strat.next_guess()
        self.assertEqual(guess, "cares")

    def test_accepts_feedback(self):
        initial_size = len(self.strat.words)
        self.strat.accept_result(
            [WRONG, WRONG, MISPLACED, CORRECT, CORRECT], "cares")
        new_size = len(self.strat.words)
        self.assertLess(new_size, initial_size)

    def test_find_highest_scoring_no_dups_excludes_all_answers(self):
        self.strat = pfs.PositionalFrequencyStrategy(dictionary=["sweet"])
        the_best_words = self.strat._find_highest_scoring_words(False)
        self.assertEqual(len(the_best_words[0]), 1,
                         F"List should be non-empty but was: {the_best_words}")
        self.assertEqual(the_best_words[0][0], "sweet")

    def test_find_highest_scoring_with_dups(self):
        self.strat = pfs.PositionalFrequencyStrategy(dictionary=["sweet"])
        the_best_words = self.strat._find_highest_scoring_words(True)
        self.assertEqual(len(the_best_words[0]), 1, "List should be non-empty")
        self.assertEqual(the_best_words[0][0], "sweet")

    def test_sissy(self):
        words = wd.load_dictionary()
        print(f"dictionary contains {len(words)} words")
        mystrat = pfs.PositionalFrequencyStrategy(
            dictionary=words,
            allow_dup_letters_after_guess=0,
            allow_letter_repetition_after_guess=2)

        self.assertEqual("sores", mystrat.next_guess())
        mystrat.accept_result(list("cwwwm"))

        mystrat.next_guess()
