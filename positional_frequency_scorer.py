import stats
import logging
import log_config
import wordle_util as wu

logger = logging.getLogger(__name__)


class PositionalFrequencyWordScorer():
    '''A strategy based on choosing the word with the highest-frequency letters in each position'''

    def __init__(self, wordlist: list[str], position_counts: list[dict[str, int]] = None):
        self.wordlist = wordlist
        self.position_counts = position_counts or stats.count_letters_by_position(
            wordlist)

    def _choose_next_word(self, allow_double_letters: bool) -> str:
        (words, score) = self._find_highest_scoring_words(allow_double_letters)
        if(words):
            return words[0]
        else:
            return None

    def _find_highest_scoring_words(self, allow_double_letters: bool) -> tuple[list[str], int]:
        # TODO: I bet itertools has a cleaner way to do this
        best_score = 0
        best_words = []

        logger.debug("finding_words, len(wordlist)=%s, allow_double_letter=%s", len(
            self.wordlist), allow_double_letters)

        for word in self.wordlist:
            if not allow_double_letters and len(word) > len(set(word)):
                continue

            frequencies = stats.extract_letter_counts_for_word(
                self.position_counts, word)
            score = sum(frequencies)
            if score > best_score:
                best_words = [word]
                best_score = score
                logger.debug("best_score=%s, word=%s", best_score, word)
            elif score == best_score:
                logger.debug("best_score=%s, word=%s", best_score, word)
                best_words.append(word)

        if best_words:
            return (best_words, best_score)
        else:
            return ([], None)

    def remove_non_matching_words(self, guess: str, letter_scores: list[str]) -> list[str]:
        new_wordlist = []
        for word in self.wordlist:
            if wu.is_possible_solution(word, guess, letter_scores):
                new_wordlist.append(word)
            else:
                for (idx, letter) in enumerate(word):
                    self.position_counts[idx][letter] -= 1

        self.wordlist = new_wordlist

    def remove_words_containing_letters(self, letters: str) -> list[str]:
        letter_set = set(letters)
        new_wordlist = []

        for word in self.wordlist:
            if letter_set.isdisjoint(word):
                new_wordlist.append(word)
            else:
                for (idx, letter) in enumerate(word):
                    self.position_counts[idx][letter] -= 1

        self.wordlist = new_wordlist
