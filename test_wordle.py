import wordle_dict as wd
import wordle as wordle
import unittest
from unittest import TestCase


class TestWordle(TestCase):

    def setUp(self) -> None:
        self.words = wd.load_dictionary()
        return super().setUp()

    def test_check_word_multi_letter_guess(self):
        (is_correct, letter_scores) = wordle.check_word(
            solution="tamed", guess="tummy")
        self.assertFalse(is_correct)
        self.assertEqual(letter_scores, [
                         wordle.CORRECT, wordle.WRONG, wordle.CORRECT, wordle.MISPLACED, wordle.WRONG])

    def test_check_word_correct(self):
        (is_correct, letter_scores) = wordle.check_word(
            solution="tamed", guess="tamed")
        self.assertTrue(is_correct)
        self.assertEqual(letter_scores, [
            wordle.CORRECT, wordle.CORRECT, wordle.CORRECT, wordle.CORRECT, wordle.CORRECT])
