import stats
import wordle_dict as wd
import unittest
from unittest import TestCase


class TestStats(TestCase):
    def setUp(self) -> None:
        self.words = wd.load_dictionary()
        return super().setUp()

    
