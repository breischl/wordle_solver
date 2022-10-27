import csv

import wordle_dict as wd
from wordle_dict import (COMBINED_WORDS_CSV, POSITION_COUNTS_CSV,
                         WORD_FREQUENCY_CSV)

letters = [chr(l) for l in range(ord('a'), ord('z') + 1)]


def count_letters_by_position(wordlist: list) -> list[dict[str, int]]:
    '''Calculate the frequency of each letter, at each position. Assumes all words are 5 letters long. 

    Returns: A list[dict], with 5 entries (one for each letter). The dictionaries are {letter:count}.
    '''
    position_counts = [
        {letter: 0 for letter in letters} for position in range(0, 5)
    ]

    for w in wordlist:
        for (idx, letter) in enumerate(w):
            position_counts[idx][letter] += 1

    return position_counts


def rank_letters_by_position(position_counts: list[dict], top_n: int = 26) -> list[tuple]:
    '''Convert a list of position counts obtained from count_letters_by_position() into a sorted list of (letter, count) tuples
    '''
    sorted_pos_counts = list()

    for pos_count in position_counts:
        sorted_count = list(pos_count.items())
        sorted_count.sort(key=lambda item: item[1], reverse=True)
        sorted_count = sorted_count[:top_n]
        sorted_pos_counts.append(sorted_count)

    return sorted_pos_counts


def extract_letter_counts_for_word(position_counts: list[dict], word: str) -> list:
    '''Extracts the frequency of each letter in the given word, using the frequency counts produced by count_letters_by_position()'''
    frequencies = list()
    for idx in range(0, 5):
        counts = position_counts[idx]
        letter = word[idx]
        frequencies.append(counts[letter])

    return frequencies


def letter_count(wordlist: list, extractor: callable) -> list[tuple[str, int]]:
    '''Extract the letter(s) of each word in the wordlist using the given function, then count occurrences of those letters

    Returns: A list of tuples (letter, count) sorted by descending value of count
    '''
    lcount = {letter: 0 for letter in letters}

    for w in wordlist:
        for l in extractor(w):
            lcount[l] += 1

    sorted_lcount = list(lcount.items())
    sorted_lcount.sort(key=lambda item: item[1], reverse=True)
    return sorted_lcount


def count_first_letters(wordlist: list) -> list[tuple[str, int]]:
    return letter_count(wordlist, lambda word: [word[0]])


def count_letter_frequency(wordlist: list) -> list[tuple[str, int]]:
    return letter_count(wordlist, lambda word: word)


def count_letter_frequency_no_dup(wordlist: list) -> list[tuple[str, int]]:
    return letter_count(wordlist, lambda word: set(word))


def write_letter_position_count_csv() -> None:
    '''Calculate the letter-position scores for each word, and write them out to a CSV file
        This is a rarely-used utility function
    '''
    words = wd.load_dictionary()
    position_counts = count_letters_by_position(words)
    word_scores = [(word, sum(extract_letter_counts_for_word(
        position_counts, word))) for word in words]
    max_score = max(word_scores, key=lambda x: x[1])[1]

    scaled_word_scores = [(ws[0], ws[1], ws[1] / max_score)
                          for ws in word_scores]

    with (open(POSITION_COUNTS_CSV, "wt", newline='') as count_file):
        cw = csv.writer(count_file, quoting=csv.QUOTE_MINIMAL)
        cw.writerow(["word", "score", "scaled_score"])
        cw.writerows(scaled_word_scores)


def read_position_counts_csv() -> list[tuple[str, int, float]]:
    with (open(POSITION_COUNTS_CSV, "r", newline='') as count_file):
        cr = csv.reader(count_file)
        next(cr)  # throw away the header row
        return [(word, int(score), float(scaled_score)) for (word, score, scaled_score) in cr]


def read_word_frequency_csv() -> list[tuple[str, int, float]]:
    with (open(WORD_FREQUENCY_CSV, "r", newline='') as freq_file):
        cr = csv.reader(freq_file)
        next(cr)  # throw away the header row
        return [(word, int(freq), float(scaled_freq)) for (word, freq, scaled_freq) in cr]


class WordScores():
    position_score: int
    scaled_position_score: int
    frequency: int
    scaled_frequency: float

    def __init__(self, pos_score: int = 0, scaled_pos_score: float = 0.00000000001, frequency: int = 0, scaled_frequency: float = 0.00000000001):
        self.position_score = pos_score
        self.scaled_position_score = scaled_pos_score
        self.frequency = frequency
        self.scaled_frequency = scaled_frequency

    def preference(self) -> float:
        return self.scaled_position_score * self.scaled_frequency


def calculate_combined_word_scores() -> dict[str, WordScores]:
    pos_counts = read_position_counts_csv()
    word_freq = read_word_frequency_csv()

    combined = {t[0]: WordScores(
        pos_score=t[1], scaled_pos_score=t[2]) for t in pos_counts}
    for (word, word_freq, scaled_word_freq) in word_freq:
        if word in combined:
            combined[word].frequency = word_freq
            combined[word].scaled_frequency = scaled_word_freq
        else:
            combined[word] = WordScores(
                frequency=word_freq, scaled_frequency=scaled_word_freq)

    return combined


def write_combined_word_scores_csv(scores: dict[str, WordScores]) -> None:
    sorted_words = sorted([(item[0], item[1])
                          for item in scores.items()], key=lambda kv: -kv[1].preference())

    with (open(COMBINED_WORDS_CSV, "wt", newline='') as count_file):
        cw = csv.writer(count_file, quoting=csv.QUOTE_MINIMAL, )
        cw.writerow(["word", "preference", "pos_score", "scaled_pos_score",
                    "frequency", "scaled_frequency"])
        for (word, scores) in sorted_words:
            cw.writerow((word, scores.preference(), scores.position_score,
                        scores.scaled_position_score, scores.frequency, scores.scaled_frequency))


def read_combined_word_scores_csv() -> list[tuple[str, int, float]]:
    with (open(COMBINED_WORDS_CSV, "r", newline='') as freq_file):
        cr = csv.reader(freq_file)
        next(cr)  # throw away the header row
        return [(word, int(pref), int(pos_score), float(scaled_pos_score), int(freq), float(scaled_pos_score)) for (word, pref, pos_score, scaled_pos_score, freq, scaled_freq) in cr]


if __name__ == "__main__":
    words = wd.load_dictionary()

    letter_pos_counts = count_letters_by_position(words)
    ranked_letters = rank_letters_by_position(letter_pos_counts, top_n=5)
    print(ranked_letters)
