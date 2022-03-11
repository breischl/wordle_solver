import positional_frequency_scorer as pfs
import argparse as arg

from wordle_strategy import WordleStrategy

parser = arg.ArgumentParser(description="Advises you how to beat Wordle")
parser.add_argument("-e", "--exploration", nargs=1, default=5, type=int,
                    help="Number of guesses to stay in exploration mode")
args = parser.parse_args()

settings = {
    "max_exploration_guesses": args.exploration
}

strat = WordleStrategy(pfs.PositionalFrequencyWordScorer(),
                       exploration_settings=settings)

guess_num = 1
while guess_num < 7:
    suggestion = strat.next_guess()

    print(f"Guess {guess_num} - I suggest '{suggestion}'")
    guess = input("What did you guess? (return if you used my suggestion)")

    if not guess:
        guess = suggestion

    result = input(
        "What was the result? wrong=>w, misplaced=>m, correct=>c, invalid word=>i, finished=>f\n")

    if len(result) == 1:
        if result[0] == "f":
            print(f"Woohoo, congrats!")
            break
        elif result[0] == "i":
            print(f"Removing '{guess}' from the dictionary...")
            guess_num -= 1
            words.remove(guess)
            # TODO: permanently remove from the dictionary file
    elif result == "ccccc":
        print(f"Woohoo, congrats!")
        break
    else:
        words = strat.accept_result(list(result), guess=guess)

    guess_num += 1
