
# POKER

A poker casino game that operates within a linux terminal created by @hansoh0 (https://www.github.com/hansoh0)


## Installation

Install requirements with pip

```
pip install -r requirements.txt
```
## How to Play
Run the program
```
hansoho@hansoho.co:~$ python3 poker.py
```
The user is prompted with a screen similar to the one shown below
```
> Select cards to hold with the number keys. [DELETE to exit/ENTER to confirm].
[ 1 ] : 10♥
[ 2 ] : A♥
[ 3 ] : 4♠
[ 4 ] : 5♣
[ 5 ] : 4♥
```
To hold certain cards within the deck, press the number key on your keyboard corresponding to the card you want held. I want to hold the two 4s for the possibility of getting a pair or three-of-a-kind so I press the number keys 3 and 4. If I dont want those card anymore I will press those number keys again to release. Your held cards will be displayed below the above interface.
```
Holding: [1]:   [2]:   [3]: 4♠  [4]:   [5]: 4♥
```

To confirm my choices, I press enter. Depending on your choices and the cards displayed in the hand, it will prompt you with one or two of multiple messages:
```
> Full House!
> Flush!
> Royal Flush!
> Straight Flush!
> Straight!
> Four of a Kind!
> Three of a Kind!
> Two Pair!
> One Pair!
```
The game will continue until the user presses the delete key, at which the program will exit.

** Requires X server to be running & requires a display env var to be set
