import stats as s
import wordle_dict as wd
import wordle as w


class GlobalFrequencyStrategy:
    '''A strategy based on choosing the word with the most high-frequency letters regardless of position'''

    def __init__(self, dictionary: list[str] = wd.load_dictionary, allow_dup_letters_after_guess: int = 2):
        self.words = dictionary
        self.allow_dup_letters_after_guess = allow_dup_letters_after_guess
        self.last_guess = None
        self.guess_num = 1

    def next_guess(self):
        next_guess = self._find_highest_scoring_word()
        self.guess_num += 1
        self.last_guess = next_guess
        return next_guess

    def accept_result(self, results: list[str], guess: str = None):
        guess = guess or self.last_guess
        self.words = w.remove_non_matching_words(self.words, guess, results)

    def _duplicate_letters_allowed(self):
        return self.guess_num > self.allow_dup_letters_after_guess

    def _find_highest_scoring_word(self) -> str:
        return self._find_highest_scoring_words(self._duplicate_letters_allowed())[0][0]

    def _find_highest_scoring_words(self, allow_dup_letters: bool) -> tuple[list[str], int]:
        letter_counts = dict(s.count_letter_frequency_no_dup(self.words))

        # TODO: I bet itertools has a cleaner way to do this
        best_score = 0
        best_words = []

        for word in self.words:
            if not allow_dup_letters and len(set(word)) != len(word):
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
        elif not allow_dup_letters:
            return self._find_highest_scoring_words(True)
        else:
            # Shouldn't really happen unless the list is empty anyway
            return (self.words[0], 0)
