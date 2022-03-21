import wordle_dict as wd
from wordle_util import *
import unittest
from unittest import TestCase


class TestWordle(TestCase):

    def setUp(self) -> None:
        self.words = wd.load_dictionary()
        return super().setUp()

    def test_check_word_multi_letter_guess(self):
        (is_correct, letter_scores) = check_word(
            solution="tamed", guess="tummy")
        self.assertFalse(is_correct)
        self.assertEqual(
            letter_scores, [CORRECT, WRONG, CORRECT, MISPLACED, WRONG])

    def test_check_word_correct(self):
        (is_correct, letter_scores) = check_word(
            solution="tamed", guess="tamed")
        self.assertTrue(is_correct)
        self.assertEqual(letter_scores, [
            CORRECT, CORRECT, CORRECT, CORRECT, CORRECT])

    def test_is_possible_solution(self):
        self.assertFalse(is_possible_solution(word="tamed", guess="tummy", letter_scores=[
            WRONG, CORRECT, CORRECT, CORRECT, CORRECT]))

        self.assertFalse(is_possible_solution(word="tamed", guess="tummy", letter_scores=[
            MISPLACED, CORRECT, CORRECT, CORRECT, CORRECT]))

        self.assertTrue(is_possible_solution(word="tumor", guess="tummr", letter_scores=[
            CORRECT, CORRECT, CORRECT, MISPLACED, CORRECT]))
