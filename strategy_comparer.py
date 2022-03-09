from statistics import mean
import wordle_dict as wd
import wordle as w
import numpy as np
from wordle_strategy import WordleStrategy
import positional_frequency_strategy as pfs
import global_frequency_strategy as gfs

words = wd.load_dictionary()


def check_strategy(strat_builder: callable) -> tuple[int, int, list[int]]:
    oracle = wd.load_oracle()
    wins = 0
    losses = 0
    guess_counts = []

    for solution in oracle:
        # print(f"Oracle contains {len(oracle)} words, dictionary contains {len(words)} words")
        strat = strat_builder(words.copy())
        num_guesses = try_solve_word(strat, solution)

        if num_guesses < 7:
            wins += 1
            guess_counts.append(num_guesses)
        else:
            losses += 1
        # print(f"Took {num_guesses} to solve '{solution}'")

    return (wins, losses, guess_counts)


def try_solve_word(strat: WordleStrategy, solution: str):
    for guess_num in range(1, 7):
        guess = strat.next_guess()
        (is_correct, result) = w.check_word(solution, guess)
        # print(
        #     f"solution {solution}, guess_num {guess_num}, guess {guess}, result {result}")

        if(is_correct):
            return guess_num
        else:
            strat.accept_result(result)

    return 7


def print_summary_stats(test_results: tuple[int, int, list[int]], strat_name: str) -> None:
    (wins, losses, guess_counts) = test_results
    win_pct = wins / (wins + losses)
    mean_guesses = np.mean(guess_counts, dtype=np.float32)
    median_guesses = np.mean(guess_counts, dtype=np.float32)

    print(
        f'{strat_name}:\nwin rate: {win_pct:0.2%},   mean guesses: {mean_guesses:#0.2f}, median guesses: {median_guesses:#0.2f}\n')


if __name__ == "__main__":
    for duplicates in range(0, 3):
        for repetition in range(0, 3):
            # print(
            #     f"Checking PositionalFrequencyStrategy, duplicates={duplicates}, repetition={repetition}")
            results = check_strategy(
                lambda w: pfs.PositionalFrequencyStrategy(dictionary=w,
                                                          allow_dup_letters_after_guess=duplicates,
                                                          allow_letter_repetition_after_guess=repetition))
            print_summary_stats(
                results, f"Positional Frequency Strategy, double letters after {duplicates} guesses, repetition after {repetition} guesses")

    for duplicates in range(0, 2):
        for repetition in range(0, 2):
            # print(
            #     f"Checking GlobalFrequencyStrategy, duplicates={duplicates}, repetition={repetition}")
            results = check_strategy(
                lambda w: gfs.GlobalFrequencyStrategy(w, duplicates, repetition))
            print_summary_stats(
                results, f"Global Frequency Strategy, double letters after {duplicates} guesses, repetition after {repetition} guesses")
