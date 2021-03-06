import csv as csv

'''Functions to handle loading and saving the dictionary from files
'''
DICTIONARY_FILE = 'words_alpha.txt'
ORACLE_FILE = 'wordle_oracle.txt'
FREQUENCY_FILE = 'word_frequency.csv'
POSITION_COUNTS_CSV = "word_position_counts.csv"
COMBINED_WORDS_CSV = "combined_word_counts.csv"
WORD_FREQUENCY_CSV = "word_frequency.csv"


def _parse_freq_line(line: str) -> tuple[str, int]:
    parts = line.split(",")
    if parts[1].isnumeric():
        return (parts[0], int(parts[1]))
    else:
        return None


def load_frequency() -> list[(str, int)]:
    '''Load the word-frequency CSV and return it as (word, score) tuples in sorted order (most common first)
    '''

    with open(FREQUENCY_FILE, mode="rt") as word_file:
        lines = [tuple for line in word_file.read().splitlines()
                 if (tuple := _parse_freq_line(line))]

    return lines


def cleanse_frequency() -> None:
    '''Read in the word frequency file, remove unneeded words (ie, length != 5), and write the result back'''
    freq_tuples = [t for t in load_frequency() if is_valid_word(t[0])]

    with open(FREQUENCY_FILE, mode="wt") as word_file:
        for t in freq_tuples:
            word_file.write(t[0])
            word_file.write(",")
            word_file.write(str(t[1]))
            word_file.write("\n")


def load_dictionary() -> list[str]:
    '''Load and return the dictionary as a list[str]
    Returns: list[str]
    '''
    with open(DICTIONARY_FILE, mode="rt") as word_file:
        words = [w for w in word_file.read().splitlines()]

    return words


def cleanse_dictionary() -> None:
    '''Read in the dictionary file, remove invalid words, and write the result back'''
    with open(DICTIONARY_FILE, mode="rt") as word_file:
        valid_words = {w for w in word_file.read().splitlines()
                       if is_valid_word(w)}

    sorted_word_list = sorted(valid_words)
    save_dictionary(sorted_word_list)


def save_dictionary(words: list[str]) -> None:
    '''Save the given list to the dictionary file
    '''

    with open(DICTIONARY_FILE, mode="wt") as word_file:
        for w in words:
            word_file.write(w)
            word_file.write("\n")


def _read_words_from_csv(file: str) -> list[str]:
    with(open(file, "r", newline='') as count_file):
        cr = csv.reader(count_file)
        next(cr)  # throw away the header row
        return [t[0] for t in cr]


def load_position_frequency_dictionary() -> list[str]:
    return _read_words_from_csv(POSITION_COUNTS_CSV)


def load_word_frequency_dictionary() -> list[str]:
    return _read_words_from_csv(WORD_FREQUENCY_CSV)


cached_combined_dict: list[str] = None

def load_combined_word_score_dictionary() -> list[str]:
    global cached_combined_dict
    if cached_combined_dict is None:
        cached_combined_dict = _read_words_from_csv(COMBINED_WORDS_CSV)

    return cached_combined_dict.copy()


def is_valid_word(w: str):
    '''Filter invalid words from the dictionary
    '''
    return len(w) == 5 and w.isalpha()


def load_oracle() -> list[str]:
    '''Load the list of all Wordle solutions'''
    with open(ORACLE_FILE, mode="rt") as word_file:
        words = [w for w in word_file.read().splitlines()]
    return words


if __name__ == "__main__":
    cleanse_dictionary()
