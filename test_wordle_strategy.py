import unittest
import wordle_strategy as ws
from wordle_strategy import WRONG
from wordle_strategy import MISPLACED
from wordle_strategy import CORRECT


class TestWordleStrategy(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_is_possible_solution(self):
        self.assertFalse(ws.is_possible_solution(word="tamed", guess="tummy", letter_scores=[
            WRONG, CORRECT, CORRECT, CORRECT, CORRECT]))

        self.assertFalse(ws.is_possible_solution(word="tamed", guess="tummy", letter_scores=[
            MISPLACED, CORRECT, CORRECT, CORRECT, CORRECT]))

        self.assertTrue(ws.is_possible_solution(word="tumor", guess="tummr", letter_scores=[
            CORRECT, CORRECT, CORRECT, MISPLACED, CORRECT]))
