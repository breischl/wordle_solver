import stats as s


class GlobalFrequencyWordScorer():
    '''A strategy based on choosing the word with the most high-frequency letters regardless of position'''

    def _choose_next_word(self, wordlist: list[str], allow_double_letters: bool) -> str:
        (words, score) = self._find_highest_scoring_words(
            wordlist, allow_double_letters)
        if(words):
            return words[0]
        else:
            return None

    def _find_highest_scoring_words(self, wordlist: list[str], allow_double_letters: bool) -> tuple[list[str], int]:
        letter_counts = dict(s.count_letter_frequency_no_dup(wordlist))

        # TODO: I bet itertools has a cleaner way to do this
        # Seems like `max()` could do it as well, but I'm not sure how to write the `key` function cleanly
        best_score = 0
        best_words = []

        for word in wordlist:
            if not allow_double_letters and len(word) > len(set(word)):
                continue

            frequencies = {letter_counts[letter] for letter in set(word)}
            score = sum(frequencies)
            if score > best_score:
                best_words = [word]
                best_score = score
            elif score == best_score:
                best_words.append(word)

        if len(best_words) > 0:
            return (best_words, best_score)
        else:
            return ([], None)
