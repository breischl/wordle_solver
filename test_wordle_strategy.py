import unittest
import wordle_strategy as ws
import positional_frequency_scorer as pfs
from wordle_strategy import WRONG, WordleStrategy
from wordle_strategy import MISPLACED
from wordle_strategy import CORRECT


class TestWordleStrategy(unittest.TestCase):
    def setUp(self) -> None:
        self.strat = WordleStrategy(pfs.PositionalFrequencyWordScorer())
        return super().setUp()

    def test_is_possible_solution(self):
        self.assertFalse(ws.is_possible_solution(word="tamed", guess="tummy", letter_scores=[
            WRONG, CORRECT, CORRECT, CORRECT, CORRECT]))

        self.assertFalse(ws.is_possible_solution(word="tamed", guess="tummy", letter_scores=[
            MISPLACED, CORRECT, CORRECT, CORRECT, CORRECT]))

        self.assertTrue(ws.is_possible_solution(word="tumor", guess="tummr", letter_scores=[
            CORRECT, CORRECT, CORRECT, MISPLACED, CORRECT]))

    def test_accepts_feedback(self):
        initial_size = len(self.strat.precision_dictionary)
        self.strat.accept_result(
            [WRONG, WRONG, MISPLACED, CORRECT, CORRECT], "arose")
        new_size = len(self.strat.precision_dictionary)
        self.assertLess(new_size, initial_size)

    # def test_handles_repetition(self):
    #     strat = ws.WordleStrategy(
    #         ["abcde", "aghez", "alemn", "qrest"], allow_dup_letters_after_guess=2, allow_letter_repetition_after_guess=2)
    #     self.assertEqual(None, strat.last_guess)
    #     self.assertEqual(4, len(strat.words))
    #     self.assertEqual(4, len(strat.shadow_dictionary))
    #     self.assertEqual(1, strat.guess_num)

    #     self.assertEqual("abcde", strat.next_guess())
    #     self.assertEqual("abcde", strat.last_guess)

    #     strat.accept_result(list("cwwwm"))
    #     self.assertEqual(2, strat.guess_num)
    #     self.assertEqual(1, len(strat.words))
    #     self.assertEqual(2, len(strat.shadow_dictionary))

    #     self.assertEqual("qrest", strat.next_guess())
    #     self.assertEqual("qrest", strat.last_guess)

    #     strat.accept_result(list("wwcww"))
    #     self.assertEqual(3, strat.guess_num)
    #     self.assertEqual(1, len(strat.words))
    #     self.assertEqual(0, len(strat.shadow_dictionary))
