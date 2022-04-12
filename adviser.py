
from letter_frequency_strategy import WordleLetterFrequencyStrategy

strat = WordleLetterFrequencyStrategy()

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
