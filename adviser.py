import argparse as arg
from wordle_strategies import build_strategy_from_name
from wordle_strategy import default_exploration_settings

parser = arg.ArgumentParser(
    description="Computer plays a game of Wordle against itself")
parser.add_argument("-t", "--strategy", type=str, default="CombinedWordScore",
                    help="Select a solver strategy, either LetterFrequency, LetterFrequencyList, WordFrequency, or CombinedWordScore")
parser.add_argument("-g", "--guesses", type=int, required=False,
                    help="Number of exploration guesses to use for strategies that support it")
args = parser.parse_args()

settings = default_exploration_settings()
if args.guesses is not None:
    settings["max_guesses"] = args.guesses

strat = build_strategy_from_name(args.strategy, settings)

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
        print("Woohoo, congrats!")
        break
    else:
        strat.accept_result(list(result), guess=guess)

    guess_num += 1
