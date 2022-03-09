import wordle_dict as wordle
import unittest
from unittest import TestCase


class TestWordleDict(unittest.TestCase):

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
