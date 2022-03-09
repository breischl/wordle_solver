import fileinput as fi
import positional_frequency_strategy as pfs

strat = pfs.PositionalFrequencyStrategy()
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
