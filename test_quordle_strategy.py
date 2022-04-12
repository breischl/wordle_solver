import unittest
import quordle_strategy as qs
import wordle_dict as wd
import wordle_util as wu
from wordle_util import WRONG, MISPLACED, CORRECT


class TestWordleStrategy(unittest.TestCase):
    def setUp(self) -> None:
        self.strat: qs.QuordleStrategy = qs.QuordleStrategy(
            wd.load_dictionary())
        return super().setUp()

    def test_accepts_feedback(self):
        initial_sizes = [
            len(self.strat.precision_word_scorers[idx].wordlist) for idx in range(0, 4)]
        self.strat.accept_results(
            ["wwwcc", "mmmww", "cwwcw", "cccww"], "arose")

        for (scorer, initial_size) in zip(self.strat.precision_word_scorers, initial_sizes):
            self.assertLess(len(scorer.wordlist), initial_size)

    def test_game(self):
        s = self.strat
        solutions = ["rayon", "polka", "torso", "faith"]
        guess = s.next_guess()

        self.assertTrue(s.exploration_mode)
        self.assertEqual(1, s.guess_num)
        self.assertEqual("cares", guess)

        pre_sizes = [len(scorer.wordlist)
                     for scorer in s.precision_word_scorers]
        results = [wu.check_word(solution, guess)[1]
                   for solution in solutions]
        s.accept_results(results, guess)

        for (scorer, pre_size) in zip(self.strat.precision_word_scorers, pre_sizes):
            self.assertLess(len(scorer.wordlist), pre_size)

        # Guess 2
        guess = s.next_guess()
        self.assertTrue(s.exploration_mode)
        self.assertEqual(2, s.guess_num)
        self.assertEqual("ponty", guess)

        results = [str(wu.check_word(solution, guess)[1])
                   for solution in solutions]
        s.accept_results(results, guess)

        for (scorer, pre_size) in zip(self.strat.precision_word_scorers, pre_sizes):
            self.assertLess(len(scorer.wordlist), pre_size)

        # Guess 3
        guess = s.next_guess()
        self.assertTrue(s.exploration_mode)
        self.assertEqual(3, s.guess_num)
        self.assertEqual("humid", guess)

        results = [wu.check_word(solution, guess)[1]
                   for solution in solutions]
        s.accept_results(results, guess)

        for (scorer, pre_size) in zip(self.strat.precision_word_scorers, pre_sizes):
            self.assertLess(len(scorer.wordlist), pre_size)

        self.assertNotEqual(None, s._choose_best_precision_scorer())
