## Double Letters ##
The actual Wordle feedback will only give one _correct_ or _misplaced_ result for each example of the letter in the solution. So if the solution only contains one instance of a letter, but the guess has two instances, then the feedback for the second instance will be _wrong_. See the third guess in _lowly1.png_, and the first two guesses in _lowly2.png_. 

Ordering does seem to matter, but correctness matters more. eg, see guess 1 in _lowly3.png_. The last 'y' in the word is correct, and the first one is marked _wrong_, even though it came first in the word. 

It appears that the checker may be scanning for correct letters first, and "consuming" them from the solution, before scoring other letters. 