import wordle_dict as wd
from wordle_util import *
from collections import defaultdict
import unittest
from unittest import TestCase


class TestWordle(TestCase):

    def setUp(self) -> None:
        self.words = wd.load_dictionary()
        return super().setUp()

    def test_count_repeats_in_solution(self):
        misplacements = count_misplaced_letters(
            "flail", [WRONG, MISPLACED, WRONG, WRONG, MISPLACED])
        self.assertEqual(misplacements['l'], 2)
        self.assertEqual(len(misplacements), 1)

        misplacements = count_misplaced_letters(
            "tummy", [WRONG, WRONG, MISPLACED, WRONG, WRONG])
        self.assertEqual(len(misplacements), 1)
        self.assertEqual(misplacements['m'], 1)

    def test_check_word_multi_letter_guess(self):
        (is_correct, letter_scores) = check_word(
            solution="tamed", guess="tummy")
        self.assertFalse(is_correct)
        self.assertEqual(
            letter_scores, [CORRECT, WRONG, CORRECT, WRONG, WRONG])

    def test_check_word_correct(self):
        (is_correct, letter_scores) = check_word(
            solution="tamed", guess="tamed")
        self.assertTrue(is_correct)
        self.assertEqual(letter_scores, [
            CORRECT, CORRECT, CORRECT, CORRECT, CORRECT])

    def test_is_possible_solution(self):
        self.assertFalse(is_possible_solution(word="tamed", guess="tummy", letter_scores=[
            WRONG, CORRECT, CORRECT, CORRECT, CORRECT], misplaced_letters=defaultdict(int)))

        self.assertFalse(is_possible_solution(word="tamed", guess="tummy", letter_scores=[
            MISPLACED, CORRECT, CORRECT, CORRECT, CORRECT], misplaced_letters=defaultdict(int)))

        self.assertTrue(is_possible_solution(word="tumor", guess="tummr", letter_scores=[
            CORRECT, CORRECT, CORRECT, MISPLACED, CORRECT], misplaced_letters=defaultdict(int)))

    def test_is_possible_solution_with_repeats(self):
        self.assertFalse(is_possible_solution(word="faulty",
                                              guess="flail",
                                              letter_scores=[
                                                  WRONG, MISPLACED, WRONG, WRONG, MISPLACED],
                                              misplaced_letters={'l': 2}))

        self.assertTrue(is_possible_solution(word="lowly",
                                             guess="flail",
                                             letter_scores=[
                                                  WRONG, MISPLACED, WRONG, WRONG, MISPLACED],

                                             misplaced_letters={'l': 2}))

        self.assertTrue(is_possible_solution(word="jolly",
                                             guess="flail",
                                             letter_scores=[
                                                  WRONG, MISPLACED, WRONG, WRONG, MISPLACED],

                                             misplaced_letters={'l': 2}))

    def test_is_possible_solution_alley_added(self):
        self.assertFalse(is_possible_solution(word="added",
                                              guess="added",
                                              letter_scores=[
                                                    CORRECT, WRONG, WRONG, CORRECT, WRONG],

                                              misplaced_letters={}))

    # from examples/lowly3.png

    def test_lowly_yampy(self):
        (is_correct, letter_scores) = check_word(
            solution="lowly", guess="yampy")
        self.assertEqual([WRONG, WRONG, WRONG, WRONG, CORRECT], letter_scores)

    # from examples/lowly2.png
    def test_lowly_brood(self):
        (is_correct, letter_scores) = check_word(
            solution="lowly", guess="brood")
        self.assertEqual(
            [WRONG, WRONG, MISPLACED, WRONG, WRONG], letter_scores)

    # from examples/lowly2.png
    def test_lowly_doors(self):
        (is_correct, letter_scores) = check_word(
            solution="lowly", guess="doors")
        self.assertEqual([WRONG, CORRECT, WRONG, WRONG, WRONG], letter_scores)

    # from examples/lowly2.png
    def test_lowly_flail(self):
        (is_correct, letter_scores) = check_word(
            solution="lowly", guess="flail")
        self.assertEqual(
            [WRONG, MISPLACED, WRONG, WRONG, MISPLACED], letter_scores)

    def test_lowly_jolly(self):
        (is_correct, letter_scores) = check_word(
            solution="lowly", guess="jolly")
        self.assertEqual(
            [WRONG, CORRECT, MISPLACED, CORRECT, CORRECT], letter_scores)

    def test_alley_added(self):
        (is_correct, letter_scores) = check_word(
            solution="added", guess="alley")
        self.assertEqual(
            [CORRECT, WRONG, WRONG, CORRECT, WRONG], letter_scores)
