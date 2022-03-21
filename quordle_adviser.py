import positional_frequency_scorer as pfs
import argparse as arg

from quordle_strategy import QuordleStrategy

parser = arg.ArgumentParser(description="Advises you how to beat Quordle")

strat = QuordleStrategy()

solutions = [None, None, None, None]

guess_num = 1
while guess_num < 10:
    suggestion = strat.next_guess()

    print(f"Guess {guess_num} - I suggest '{suggestion}'")
    guess = input("What did you guess? (return if you used my suggestion)")

    if not guess:
        guess = suggestion

    results = []
    for (idx, sol) in enumerate(solutions):
        idx_1 = idx + 1
        if sol is None:
            result = input(
                f"What was the result for word {idx_1}? wrong=>w, misplaced=>m, correct=>c\n")
            results.append(list(result))

            if(result == "ccccc"):
                solutions[idx] = guess
        else:
            print(f"We already solved word {idx_1}, it was {solutions[idx]}")
            results.append(None)

    if all([s is not None for s in solutions]):
        print("You won them all, congrats!")
        print(f"The solutions were: {str.join(', ', solutions)}")
        break
    else:
        words = strat.accept_results(results, guess=guess)

    guess_num += 1
