import fileinput as fi
import wordle_dict as wordle
import wordle as wordle
import stats as stats

words = wordle.load_dictionary()
stdin = fi.input()
print(f"Loaded dictionary of {len(words)} words")

guess_num = 1
while guess_num < 7:
    suggestion = stats.find_highest_scoring_word(words, (guess_num > 3))
    
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
        words = wordle.remove_non_matching_words(words, guess, list(result))

    guess_num += 1
