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

    # print(f"Oracle contains {len(oracle)} words")

    for solution in oracle:
        strat = strat_builder(words.copy(), 2)
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
        # print(f"solution={solution}, guess={guess}, result={str.join('', result)}")
        if(is_correct):
            return guess_num
        else:
            strat.accept_result(result)

    return 7


def print_summary_stats(test_results: tuple[int, int, list[int]], strat_name: str) -> None:
    (wins, losses, guess_counts) = test_results
    win_pct = wins / (wins + losses) * 100
    mean_guesses = np.mean(guess_counts, dtype=np.int16)
    median_guesses = np.mean(guess_counts, dtype=np.int16)

    print(
        f'Strategy {strat_name}:\nwins: {wins}, losses: {losses}, win rate: {win_pct}\nguesses to win mean: {mean_guesses}, median: {median_guesses}')


if __name__ == "__main__":
    print("Checking PositionalFrequencyStrategy")
    results = check_strategy(pfs.PositionalFrequencyStrategy)
    print_summary_stats(results, "Positional Frequency")

    print("Checking GlobalFrequencyStrategy")
    results = check_strategy(gfs.GlobalFrequencyStrategy)
    print_summary_stats(results, "Global Frequency")
