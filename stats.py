import wordle_dict as wordle
import numpy as np
import matplotlib.pyplot as plt

words = wordle.load_dictionary()
letters = [chr(l) for l in range(ord('a'), ord('z')+1)]


def count_letters_by_position(wordlist: list) -> list:
    '''Calculate the frequency of each letter, at each position. Assumes all words are 5 letters long. 

    Returns: A list[dict], with 5 entries (one for each letter). The dictionaries are {letter:count}.
    '''
    position_counts = [
        {letter: 0 for letter in letters} for position in range(0, 5)
    ]

    for w in wordlist:
        for idx in range(0, 5):
            letter = w[idx]
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


def find_highest_scoring_word(wordlist: list, allow_dup_letters: bool) -> str:
    return find_highest_scoring_words(wordlist, allow_dup_letters)[0][0]


def find_highest_scoring_words(wordlist: list, allow_dup_letters: bool) -> list[tuple[str, int]]:
    position_counts = count_letters_by_position(wordlist)

    # TODO: I bet itertools has a cleaner way to do this
    best_score = 0
    best_words = []

    for word in wordlist:
        if not allow_dup_letters and len(set(word)) != len(word):
            continue

        frequencies = extract_letter_counts_for_word(position_counts, word)
        score = sum(frequencies)
        if score > best_score:
            best_words = [word]
            best_score = score
        elif score == best_score:
            best_words.append(word)

    if len(best_words) > 0:
        return (best_words, best_score)
    elif allow_dup_letters:
        return find_highest_scoring_words(wordlist, True)
    else:
        # Shouldn't really happen unless the list is empty anyway
        return (wordlist[0], 0)


def letter_count(wordlist: list, extractor: callable) -> list:
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


def count_first_letters(wordlist: list) -> list:
    return letter_count(wordlist, lambda word: [word[0]])


def count_letter_frequency(wordlist: list) -> list:
    return letter_count(wordlist, lambda word: word)


def count_letter_frequency_no_dup(wordlist: list) -> list:
    return letter_count(wordlist, lambda word: set(word))


def plot_letter_histogram(lcounts: list, name: str) -> None:
    fig = plt.figure(num=name)
    ax = fig.add_subplot()

    x = range(26)
    ax.bar(x, [lc[1] for lc in lcounts], width=0.8,
           color='g', alpha=0.5, align='center')
    ax.set_xticks(x)
    ax.set_xticklabels([t[0] for t in lcounts])
    ax.tick_params(axis='x', direction='out')
    ax.set_xlim(-0.5, 25.5)
    ax.yaxis.grid(True)
    ax.set_ylabel('Letter count')


if __name__ == "__main__":
    # plot_letter_histogram(count_first_letters(words), "First letters")
    # plot_letter_histogram(count_letter_frequency(words), "All letters")
    # plot_letter_histogram(count_letter_frequency_no_dup(
    #     words), "All letters deduped")
    # plt.show()

    letter_pos_counts = count_letters_by_position(words)
    ranked_letters = rank_letters_by_position(letter_pos_counts, top_n=5)
    print(ranked_letters)

    print(find_highest_scoring_words(words, allow_dup_letters=True))
    print(find_highest_scoring_words(words, allow_dup_letters=False))
