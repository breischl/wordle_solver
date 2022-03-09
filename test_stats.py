import stats
import wordle_dict as wordle
import unittest
from unittest import TestCase


class TestStats(TestCase):
    def setUp(self) -> None:
        self.words = wordle.load_dictionary()
        return super().setUp()

    def test_find_highest_scoring_words_basic(self):
        the_best_words = stats.find_highest_scoring_words(self.words, False)
        self.assertTrue(the_best_words, "List should be non-empty")
        self.assertEqual(the_best_words[0][0], "cares")
