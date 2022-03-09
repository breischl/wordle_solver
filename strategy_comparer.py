from statistics import mean
import wordle_dict as wd
import wordle as w
import numpy as np
import argparse as arg
from wordle_strategy import WordleStrategy
import positional_frequency_strategy as pfs
import global_frequency_strategy as gfs

words = wd.load_dictionary()


def check_strategy(strat_builder: callable) -> tuple[int, int, list[int]]:
    oracle = wd.load_oracle()
    wins = 0
    losses = 0
    guess_counts = []
    misses = []

    for solution in oracle:
        # print(f"Oracle contains {len(oracle)} words, dictionary contains {len(words)} words")
        strat = strat_builder(words.copy())
        num_guesses = try_solve_word(strat, solution)

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

        (is_correct, result) = w.check_word(solution, guess)
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
parser.add_argument("--strategies", type=str, default="All",
                    choices=["PositionalFrequency", "GlobalFrequency", "All"])
parser.add_argument("-dn", "--duplicates_min", default=1, type=int,
                    help="Min number of guesses before suggesting words containing the same letter more than once")
parser.add_argument("-dx", "--duplicates_max", default=4, type=int,
                    help="Max number of guesses before suggesting words containing the same letter more than once")
parser.add_argument("-rn", "--repetition_min", default=1, type=int,
                    help="Min number of guesses before suggesting words containing previously-guessed letters. ie, all letters suggested will be new until this many guesses.")
parser.add_argument("-rx", "--repetition_max", default=1, type=int,
                    help="Max number of guesses before suggesting words containing previously-guessed letters. ie, all letters suggested will be new until this many guesses.")
args = parser.parse_args()

strategies = []
if "all" in args.strategies:
    args.strategies = ["PositionalFrequency", "GlobalFrequency"]
if "PositionalFrequency" in args.strategies:
    strategies.append(("Positional Frequency", lambda w: pfs.PositionalFrequencyStrategy(dictionary=w,
                                                                                         allow_dup_letters_after_guess=duplicates,
                                                                                         allow_letter_repetition_after_guess=repetition)))
if "GlobalFrequency" in args.strategies:
    strategies.append(("Global Frequency", lambda w: gfs.GlobalFrequencyStrategy(dictionary=w,
                                                                                 allow_dup_letters_after_guess=duplicates,
                                                                                 allow_letter_repetition_after_guess=repetition)))


for (strat_name, strat_builder) in strategies:
    for duplicates in range(args.duplicates_min, args.duplicates_max + 1):
        for repetition in range(args.repetition_min, args.repetition_max + 1):
            results = check_strategy(strat_builder)
            print_summary_stats(
                results, f"{strat_name} Strategy, double letters after {duplicates} guesses, repetition after {repetition} guesses")
