'''Functions to handle loading and saving the dictionary from files
'''
DICTIONARY_FILE = 'words_alpha.txt'
ORACLE_FILE = 'wordle_oracle.txt'


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
        valid_words = {w
                       for w in word_file.read().splitlines()
                       if is_valid_word(w)}

    save_dictionary(valid_words)


def save_dictionary(words: list[str]) -> None:
    '''Save the given list to the dictionary file
    '''

    with open(DICTIONARY_FILE, mode="wt") as word_file:
        for w in words:
            word_file.write(w)
            word_file.write("\n")


def is_valid_word(w: str):
    '''Filter invalid words from the dictionary
    '''
    return len(w) == 5 and w.isalpha()


def load_oracle() -> list[str]:
    '''Load the list of all Wordle solutions'''
    with open(ORACLE_FILE, mode="rt") as word_file:
        words = [w for w in word_file.read().splitlines()]
    return words
