import wordle_dict as wd
import numpy as np
import argparse as arg
from wordle_util import check_word
import logging
from wordle_strategies import build_strategy_from_name
import log_config  # import does logging config

log = logging.getLogger(__name__)


def check_strategy(strat_builder: callable) -> tuple[int, int, list[tuple[str, int]]]:
    oracle = wd.load_oracle()
    wins = 0
    losses = 0
    guess_counts = []
    misses = []

    for solution in oracle:
        num_guesses = try_solve_word(strat_builder(), solution)

        if num_guesses < 7:
            wins += 1
            guess_counts.append((solution, num_guesses))
        else:
            losses += 1
            misses.append(solution)

    return (wins, losses, guess_counts, sorted(misses))


def try_solve_word(strat, solution: str):
    for guess_num in range(1, 7):
        guess = strat.next_guess()
        if guess:
            (is_correct, result) = check_word(solution, guess)
        else:
            return 7

        if is_correct:
            return guess_num
        else:
            strat.accept_result(result, guess)

    return 7


def print_summary_stats(test_results: tuple[int, int, list[tuple[str, int]]], strat_name: str) -> None:
    (wins, losses, successes, missed_words) = test_results
    win_pct = wins / (wins + losses)
    mean_guesses = np.mean([c[1] for c in successes], dtype=np.float32)
    median_guesses = np.median([c[1] for c in successes])

    print(f'{strat_name}')
    print(
        f'win rate: {win_pct:0.2%}, mean guesses: {mean_guesses:#0.2f}, median guesses: {median_guesses:#0.2f}')
    print(f'wins: {wins}, losses: {losses}\n')
    print(f'missed words: {missed_words}')
    # print("Successful guess counts:")

    # for (solution, guess_count) in successes:
    #     print(f"{solution}: {guess_count}")


parser = arg.ArgumentParser(
    description="Run the given strategy & settings against all known Wordle solutions")
parser.add_argument("-gn", "--guesses_min", default=3, type=int,
                    help="Min number of guesses to stay in exploration mode")
parser.add_argument("-gx", "--guesses_max", default=5, type=int,
                    help="Max number of guesses to stay in exploration mode")
parser.add_argument("-t", "--strategy",
                    default="LetterFrequencyStrategy", type=str)
parser.add_argument("-f", "--firstword", default=None, type=str,
                    help="Force strategies to use the given first word")
args = parser.parse_args()

for explore_guesses in range(args.guesses_min, args.guesses_max + 1):
    settings = {
        "max_guesses": explore_guesses,
        "first_word": args.firstword
    }
    print(f"Starting run for guesses={explore_guesses}")
    results = check_strategy(
        lambda: build_strategy_from_name(args.strategy, settings))
    print_summary_stats(
        results, f"Exploration mode for {explore_guesses} guesses")
