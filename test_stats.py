import stats
import wordle_dict as wordle
import unittest
from unittest import TestCase


class TestStats(TestCase):
    def setUp(self) -> None:
        self.words = wordle.load_dictionary()
        return super().setUp()

    
