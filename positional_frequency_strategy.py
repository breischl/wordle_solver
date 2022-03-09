import stats
import wordle_strategy as ws


class PositionalFrequencyStrategy(ws.WordleStrategy):
    '''A strategy based on choosing the word with the highest-frequency letters in each position'''

    def _choose_next_word(self, allow_dup_letters: bool) -> str:
        (words, score) = self._find_highest_scoring_words(allow_dup_letters)
        if(words):
            return words[0]
        else:
            return None

    def _find_highest_scoring_words(self, allow_dup_letters: bool) -> tuple[list[str], int]:
        position_counts = stats.count_letters_by_position(self.words)

        # TODO: I bet itertools has a cleaner way to do this
        best_score = 0
        best_words = []

        for word in self.words:
            if not allow_dup_letters and len(set(word)) != len(word):
                continue

            frequencies = stats.extract_letter_counts_for_word(
                position_counts, word)
            score = sum(frequencies)
            if score > best_score:
                best_words = [word]
                best_score = score
            elif score == best_score:
                best_words.append(word)

        if len(best_words) > 0:
            return (best_words, best_score)
        elif not allow_dup_letters:
            return self._find_highest_scoring_words(True)
        else:
            return ([], None)
            # return (self.words[0], 0)
