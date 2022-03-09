# wordle_solver
A set of scripts around solving the popular Wordle puzzle game. The best I've managed with this gets the correct answer 97.7% of the time. 

This is mostly a learning exercise for me - it's my first non-trivial Python script. Please judge the code quality accordingly. :) 

## Usage
`python adviser.py` will launch a simple console app that will advise you on what to guess, and accept results to update future guesses. For example:
```
ython adviser.py
Guess 1 - I suggest 'cares'
What did you guess? (return if you used my suggestion)
cares
What was the result? wrong=>w, misplaced=>m, correct=>c, invalid word=>i, finished=>f
wwwww
Guess 2 - I suggest 'ponty'
What did you guess? (return if you used my suggestion)
```

`python wordle.py` will choose a random word and the computer will play against itself. Use the `-s` commandline argument to choose the solution word. For example:
```
python wordle.py -s 
python wordle.py -s fiver
Solution is 'fiver'
I'll guess 'cares'
'cares' was wrong, letter scores are: wwmcw
I'll guess 'ponty'
'ponty' was wrong, letter scores are: wwwww
I'll guess 'humid'
'humid' was wrong, letter scores are: wwwmw
I'll guess 'fiver'
'fiver' is correct, I win!
```

## What's It Doing?
The script has a dictionary of 5-letter words. For each of the five letter positions, it calculates how many of those words have each letter. So we have `5 * 26 = 130` letter-position frequencies. Then it computes a score for each word that consists of the the frequency for each letter of that word. The highest scoring word is chosen as the guess. 

The feedback is used to eliminate any words that could not possibly be a solution. Then the we repeat the entire process with the now-smaller dictionary. 

In order to winnow out incorrect letters quickly, the first two guesses are not allowed to have the same letter twice in the same word. Also the second guess is not allowed to repeat any letters from the first guess. For guess 3 and later, it will choose the most likely word as already outlined. 