import argparse as arg
from wordle_strategies import build_strategy_from_name

parser = arg.ArgumentParser(
    description="Computer plays a game of Wordle against itself")
parser.add_argument("-t", "--strategy", type=str, default="CombinedWordScore",
                    help="Select a solver strategy, either LetterFrequency, LetterFrequencyList, WordFrequency, or CombinedWordScore")
parser.add_argument("-g", "--guesses", type=int, default=4,
                    help="Number of exploration guesses to use for strategies that support it")
args = parser.parse_args()

strat = build_strategy_from_name(args.strategy, {"num_guesses": args.guesses})

guess_num = 1
while guess_num < 7:
    suggestion = strat.next_guess()

    if not suggestion:
        print("I have no other ideas, sorry!")
        exit()

    print(f"Guess {guess_num} - I suggest '{suggestion}'")
    guess = input("What did you guess? (return if you used my suggestion)")

    if not guess:
        guess = suggestion

    result = input(
        "What was the result? wrong=>w, misplaced=>m, correct=>c\n")

    if result == "ccccc":
        print(f"Woohoo, congrats!")
        break
    else:
        words = strat.accept_result(list(result), guess=guess)

    guess_num += 1
