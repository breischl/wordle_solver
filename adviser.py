from ast import Store
import fileinput as fi
import positional_frequency_strategy as pfs
import argparse as arg

parser = arg.ArgumentParser(description="Advises you how to beat Wordle")
parser.add_argument("-d", "--duplicates", nargs=1, default=5, type=int,
                    help="Number of guesses before suggesting words containing the same letter more than once")
parser.add_argument("-r", "--repetition", nargs=1, default=5, type=int,
                    help="Number of guesses before suggesting words containing previously-guessed letters. ie, all letters suggested will be new until this many guesses.")
args = parser.parse_args()

strat = pfs.PositionalFrequencyStrategy(
    allow_dup_letters_after_guess=args.duplicates, allow_letter_repetition_after_guess=args.repetition)
stdin = fi.input()

guess_num = 1
while guess_num < 7:
    suggestion = strat.next_guess()

    print(f"Guess {guess_num} - I suggest '{suggestion}'")
    print(f"What did you guess? (return if you used my suggestion)")
    guess = stdin.readline().rstrip()

    if len(guess) == 0:
        guess = suggestion

    print(f"What was the result? wrong=>w, misplaced=>m, correct=>c, invalid word=>i, finished=>f")
    result = stdin.readline().rstrip()

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
