import wordle_dict as wd
import unittest
from unittest import TestCase


class TestWordleDict(unittest.TestCase):

    def setUp(self) -> None:
        self.words = wd.load_dictionary()
        return super().setUp()

    def test_dictionary_loaded(self):
        self.assertNotEqual(len(self.words), 0)
        self.assertTrue("serai" in self.words)

    def test_is_valid_word(self):
        self.assertTrue(wd.is_valid_word("serai"))
        self.assertTrue(wd.is_valid_word("bonds"))

        self.assertFalse(wd.is_valid_word("1name"))
        self.assertFalse(wd.is_valid_word("bonded"))
        self.assertFalse(wd.is_valid_word("abba"))
        self.assertFalse(wd.is_valid_word("abba\n"))
