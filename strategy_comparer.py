from statistics import mean
import wordle_dict as wd
import numpy as np
import argparse as arg
from wordle_strategy import WordleStrategy
from wordle_util import check_word
import positional_frequency_scorer as pfs
import global_frequency_scorer as gfs


def check_strategy(strat_builder: callable) -> tuple[int, int, list[int]]:
    oracle = wd.load_oracle()
    wins = 0
    losses = 0
    guess_counts = []
    misses = []

    for solution in oracle:
        # print(f"Oracle contains {len(oracle)} words, dictionary contains {len(words)} words")
        num_guesses = try_solve_word(strat_builder(), solution)

        if num_guesses < 7:
            wins += 1
            guess_counts.append(num_guesses)
        else:
            losses += 1
            misses.append(solution)
        # print(f"Took {num_guesses} to solve '{solution}'")

    return (wins, losses, guess_counts, sorted(misses))


def try_solve_word(strat: WordleStrategy, solution: str):
    for guess_num in range(1, 7):
        guess = strat.next_guess()
        if not guess:
            print(
                f"Bad guess for solution {solution}, guess number {guess_num}")
            quit()

        (is_correct, result) = check_word(solution, guess)
        # print(
        #     f"solution {solution}, guess_num {guess_num}, guess {guess}, result {result}")

        if(is_correct):
            return guess_num
        else:
            strat.accept_result(result)

    return 7


def print_summary_stats(test_results: tuple[int, int, list[int]], strat_name: str) -> None:
    (wins, losses, guess_counts, missed_words) = test_results
    win_pct = wins / (wins + losses)
    mean_guesses = np.mean(guess_counts, dtype=np.float32)
    median_guesses = np.mean(guess_counts, dtype=np.float32)

    print(f'{strat_name}')
    print(
        f'win rate: {win_pct:0.2%}, mean guesses: {mean_guesses:#0.2f}, median guesses: {median_guesses:#0.2f}')
    print(f'wins: {wins}, losses: {losses}\n')
    print(f'missed words: {missed_words}')


parser = arg.ArgumentParser(
    description="Run the given strategy & settings against all known Wordle solutions")
parser.add_argument("-gn", "--guesses_min", default=3, type=int,
                    help="Min number of guesses to stay in exploration mode")
parser.add_argument("-gx", "--guesses_max", default=5, type=int,
                    help="Max number of guesses to stay in exploration mode")
args = parser.parse_args()

words = wd.load_dictionary()

for explore_guesses in range(args.guesses_min, args.guesses_max + 1):
    settings = {
        "max_guesses": explore_guesses
    }
    print(f"Starting run for guesses={explore_guesses}")
    results = check_strategy(lambda: WordleStrategy(
        exploration_settings=settings, dictionary=words.copy()))
    print_summary_stats(
        results, f"Exploration mode for {explore_guesses} guesses")
