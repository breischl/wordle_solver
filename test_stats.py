import stats
import wordle_dict as wordle
import unittest
from unittest import TestCase


class TestStats(TestCase):
    def setUp(self) -> None:
        self.words = wordle.load_dictionary()
        return super().setUp()

    def test_find_highest_scoring_words_basically_works(self):
        the_best_words = stats.find_highest_scoring_words(self.words, False)
        self.assertTrue(the_best_words[0], "List should be non-empty")
        self.assertEqual(the_best_words[0][0], "cares")

    def test_find_highest_scoring_no_dups_excludes_all_answers(self):
        tiny_dictionary = ["sweet"]
        the_best_words = stats.find_highest_scoring_words(
            tiny_dictionary, False)
        self.assertEqual(len(the_best_words[0]), 1,
                         F"List should be non-empty but was: {the_best_words}")
        self.assertEqual(the_best_words[0][0], "sweet")

    def test_find_highest_scoring_with_dups(self):
        tiny_dictionary = ["sweet"]
        the_best_words = stats.find_highest_scoring_words(
            tiny_dictionary, True)
        self.assertEqual(len(the_best_words[0]), 1, "List should be non-empty")
        self.assertEqual(the_best_words[0][0], "sweet")
