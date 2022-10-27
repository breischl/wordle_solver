# wordle_solver
A set of scripts around solving the popular Wordle puzzle game. The best I've managed with this gets the correct answer over 99% of the time. 

This is mostly a learning exercise for me - it's my first non-trivial Python script. It also went through a lot of revisions trying out different guessing strategies, which did not help to keep things well-factored. Please judge the code quality accordingly. :) In particular there are a lot of linting warnings and errors that I should probably fix, but probably won't. 

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
The following describes the "LetterFrequency" strategy that I was using. A later version changed this somewhat, to include word frequency in actual English usage. But I don't feel like rewriting this whole section since most likely nobody will ever read it. 

The script has a dictionary of 5-letter words. For each of the five letter positions, it calculates how many of those words have each letter. So we have `5 positions * 26 letters = 130 letter-position` scores. Then it computes a score for each word that consists of the the frequency for each letter of that word. The highest scoring word is chosen as the guess. 

The feedback is used to eliminate any words that could not possibly be a solution. Then the we repeat the entire process with the now-smaller dictionary. 

In order to winnow out incorrect letters quickly, the first few guesses are not allowed to have the same letter twice in the same word, and also are not allowed to reuse letters across words (ie, each letter of each word will be unique) provided the dictionary is not exhausted. These are tweakable commandline parameters to the scripts - testing showed that `5` is the best value for each, and is therefore the default. 

Tangentially, this means that it will always guess "cares" to start with, and _nearly_ always follow up with "ponty" and "humid". Those words are not written into the code anywhere, it's just what falls out of the algorithm. The first guess depends entirely on the dictionary because there is no feedback yet. The second two guesses have some feedback, but will ignore it nearly always because of the latter optimization. 

[This article](https://towardsdatascience.com/a-frequency-analysis-on-wordle-9c5778283363) outlines a similar-ish approach, though it's only applied for the first guess and does some different calculations to normalize the metric. 

## Where's the Dictionary From?
It's from the Javascript code of the Wordle web app. I believe it's the dictionary used by the app itself, but I didn't read the code enough to verify that. 

## Mellor Strategies
[An article appeared](https://www.9news.com/article/news/local/zevely-zone/five-magic-words-that-will-solve-wordle/509-fec2b387-5202-4d74-8c47-fde9221a82c1#l30tu0p44eve1xn6njh) about a strategy from noted crossword afficionado Myles Mellor, which claimed at various points to solve Wordle "every time", "99.5% of the time" or to find the letters 99.5% of the time. The strategy boils down to using the same five words to start with, and attempting to guess the final word using the sixth (and only remaining) guess. 

The `StrictMellorStrategy` was implemented to find out how often this strategy would result in a single possible word remaining at the sixth guess. This turned out to be a disappointing 84.37% of the time.

In the remainder of the cases there were multiple possible words available at the sixth guess. For example "angle" and "angel", or "ample" and "maple". The `StrictMellorStrategy` just gives up in this case. The `LaxMellorStrategy` falls back to the `CombinedWordScoreStrategy` which was found to be ideal previously - this combination is successful 96.71% of the time, a respectable but not great score compared to other options. It also takes 6 guesses to find the word in every case, except for when the word happens to be one of the five "pre-programmed" start words. 

Overall the "Mellor strategy" appears strictly inferior to other strategies available.