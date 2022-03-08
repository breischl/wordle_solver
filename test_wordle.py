import wordle
import unittest
from unittest import TestCase


class TestWordle(unittest.TestCase):

    def setUp(self) -> None:
        self.words = wordle.load_dictionary()
        return super().setUp()

    def test_dictionary_loaded(self):
        self.assertNotEqual(len(self.words), 0)
        self.assertTrue("serai" in self.words)

    def test_is_valid_word(self):
        self.assertTrue(wordle.is_valid_word("serai"))
        self.assertTrue(wordle.is_valid_word("bonds"))

        self.assertFalse(wordle.is_valid_word("1name"))
        self.assertFalse(wordle.is_valid_word("bonded"))
        self.assertFalse(wordle.is_valid_word("abba"))
        self.assertFalse(wordle.is_valid_word("abba\n"))

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

    def test_is_possible_solution(self):
        self.assertFalse(wordle.is_possible_solution(word="tamed", guess="tummy", letter_scores=[
            wordle.WRONG, wordle.CORRECT, wordle.CORRECT, wordle.CORRECT, wordle.CORRECT]))

        self.assertFalse(wordle.is_possible_solution(word="tamed", guess="tummy", letter_scores=[
            wordle.MISPLACED, wordle.CORRECT, wordle.CORRECT, wordle.CORRECT, wordle.CORRECT]))

        self.assertTrue(wordle.is_possible_solution(word="tumor", guess="tummr", letter_scores=[
            wordle.CORRECT, wordle.CORRECT, wordle.CORRECT, wordle.MISPLACED, wordle.CORRECT]))
