# wordle_solver
A set of scripts around solving the popular Wordle puzzle game. The best I've managed with this gets the correct answer over 97% of the time. 

This is mostly a learning exercise for me - it's my first non-trivial Python script. Please judge the code quality accordingly. :) 

## Usage
`python adviser.py` will launch a simple console app that will advise you on what to guess, and accept results to update future guesses. For example:
```
python adviser.py
Guess 1 - I suggest 'cares'
What did you guess? (return if you used my suggestion)
cares
What was the result? wrong=>w, misplaced=>m, correct=>c
wwwww
Guess 2 - I suggest 'ponty'
What did you guess? (return if you used my suggestion)
```

`python wordle.py` will choose a random word and the computer will play against itself. Use the `-s` commandline argument to choose the solution word. For example:
```
python wordle.py -s aging
Solution is 'aging'
'cares' was wrong
'ponty' was wrong
'humid' was wrong
'ligan' was wrong
'aging' is correct, I win!
```

## Quordle
I also implemented a version for [Quordle](https://www.quordle.com/), which is roughly like solving 4 Wordles at once. It's a little bit rougher, and I didn't test the success rate as much, but you can use it if you like. 

```
## Computer plays against itself
python quordle.py

## Tells you how to play
python quordle_adviser.py
```


## What's It Doing?
The script has a dictionary of 5-letter words. For each of the five letter positions, it calculates how many of those words have each letter. So we have `5 positions * 26 letters = 130 letter-position` scores. Then it computes a score for each word that consists of the the frequency for each letter of that word. The highest scoring word is chosen as the guess. 

The feedback is used to eliminate any words that could not possibly be a solution. Then the we repeat the entire process with the now-smaller dictionary. 

In order to winnow out incorrect letters quickly, the first few guesses are not allowed to have the same letter twice in the same word, and also are not allowed to reuse letters across words (ie, each letter of each word will be unique) provided the dictionary is not exhausted. These are tweakable commandline parameters to the scripts - testing showed that `5` is the best value for each, and is therefore the default. 

Tangentially, this means that it will always guess "cares" to start with, and _nearly_ always follow up with "ponty" and "humid". Those words are not written into the code anywhere, it's just what falls out of the algorithm. The first guess depends entirely on the dictionary because there is no feedback yet. The second two guesses have some feedback, but will ignore it nearly always because of the latter optimization. 

[This article](https://towardsdatascience.com/a-frequency-analysis-on-wordle-9c5778283363) outlines a similar-ish approach, though it's only applied for the first guess and does some different calculations to normalize the metric. 

## Where's the Dictionary From?
It's from the Javascript code of the Wordle web app. I believe it's the dictionary used by the app itself, but I didn't read the code enough to verify that. 