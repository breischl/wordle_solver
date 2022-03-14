import stats
import logging
import log_config

logger = logging.getLogger(__name__)


class PositionalFrequencyWordScorer():
    '''A strategy based on choosing the word with the highest-frequency letters in each position'''

    def _choose_next_word(self, wordlist: list[str], allow_double_letters: bool) -> str:
        (words, score) = self._find_highest_scoring_words(
            wordlist, allow_double_letters)
        if(words):
            return words[0]
        else:
            return None

    def _find_highest_scoring_words(self, wordlist: list[str], allow_double_letters: bool) -> tuple[list[str], int]:
        # TODO: Recalculating this from scratch every time is painful. It would be faster to instead calculate it once, and then update as words are removed
        position_counts = stats.count_letters_by_position(wordlist)

        # TODO: I bet itertools has a cleaner way to do this
        best_score = 0
        best_words = []

        logger.debug("finding_words, len(wordlist)=%s, allow_double_letter=%s", len(
            wordlist), allow_double_letters)

        for word in wordlist:
            if not allow_double_letters and len(word) > len(set(word)):
                continue

            frequencies = stats.extract_letter_counts_for_word(
                position_counts, word)
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
