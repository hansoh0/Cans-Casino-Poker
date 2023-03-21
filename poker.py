#! /usr/bin/env python3

"""
author: saucecan
description: a poker casino game that runs within a linux terminal
"""
import random, os, signal, termios, sys, tty, time
from pynput import keyboard

# Set OG terminal settings for reset
original_settings = termios.tcgetattr(sys.stdin)

class Poker:

    held = {1: '', 2: '', 3: '', 4: '', 5: ''}
    IO = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    def __init__(self):
        self.hand = self.create_hand()

    """
    Generates a random card
    var suits : char list is the suits as unicode
    var ranks : str list is the ranks of the cards
    return card : str is the rank and suit of a card as a string
    """
    def generate_card(self):
        suits = ["\u2663", "\u2665","\u2666", "\u2660"]
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A', 'K', 'Q', 'J']

        # Select a random suit and rank from the lists
        suit = random.choice(suits)
        rank = random.choice(ranks)
        card = rank + suit
        return card

    """
   Creates a hand to display to the user
   var hand : dict is the hand outline
   return hand : dict with cards in the value placeholder
   """
    def create_hand(self):
        # Hand
        hand = {1: '', 2: '', 3: '', 4: '', 5: ''}
        # Construct and print the card
        for i in range(1, 6):
            while True:
                card = self.generate_card()
                if card in hand.values():
                    continue
                else:
                    hand[i] = card
                    break
        self.format_hand(hand)
        return hand


    """
    Main Game Interface
    param hand : dict that contains the cards mapped to the numbers 1-5
    """
    def format_hand(self, hand):
        print("> Select cards to hold with the number keys. [DELETE to exit/ENTER to confirm].")
        for key in hand:
            print ("[",key,"]",":",hand[key])

    """
    Determines if valid poker hands are found within the hand
    var stack : str list of the cards
    var tuped_cards : str tup of the card stack
    var ranks : str list of ranks in the hand
    var suits : str list of suits in the hand
    var straight_ranks : dict of ranks with numerical values assigned to them
    var ranks_int : int list of rank values
    """
    def determine_match(self):
        stack =[]
        for key in Poker.hand:
            stack.append(Poker.hand[key])
        tuped_cards = [(card[:-1], card[-1]) for card in stack]

        # sort tuped_cards by rank in descending order
        tuped_cards.sort(reverse=True)

        # get list of ranks and suits
        ranks = [card[0] for card in tuped_cards]
        suits = [card[1] for card in tuped_cards]


        # check for full house
        if [ranks.count(rank) for rank in ranks].count(3) == 1 and [ranks.count(rank) for rank in ranks].count(2) == 1:
            print('> Full House!')

        # check for flush
        if len(set(suits)) == 1:
            print('> Flush!')

        straight_ranks = {'K': 13, 'Q': 12, 'J': 11, '10': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2, 'A': 1}
        ranks_int = [straight_ranks[rank] for rank in ranks]

        # Check for royal flush
        if set(ranks).intersection({'A', 'K', 'Q', 'J', '10'}) == {'A', 'K', 'Q', 'J', '10'}:
                print('> Royal Flush!')

        # Checking for straight and straight flush
        if max(ranks_int) - min(ranks_int) == 4 and len(set(ranks_int)) == 5:
            if '4' not in ranks:
                print('> Straight Flush!')
            else:
                print('> Straight!')

        # check for four of a kind X
        if 4 in [ranks.count(rank) for rank in ranks]:
            print('> Four of a Kind!')

        # check for three of a kind X
        if 3 in [ranks.count(rank) for rank in ranks]:
            if 2 in [ranks.count(rank) for rank in ranks]:
                print('> Full House!')
            else:
                print('> Three of a Kind!')

        # check for two pair X
        if [ranks.count(rank) for rank in ranks].count(2) == 4:
            print('> Two Pair!')

        # check for one pair X
        if [ranks.count(rank) for rank in ranks].count(2) == 2:
            print('> One Pair!')

    """
    Takes a hand, determines which cards are NOT held by utilizing the IO dictionary, and replaces those cards with a new card
    """
    def modify_hand(self):
        for key in Poker.IO:
            if Poker.IO.get(int(key)) == 0:
                while True:
                    card = Poker.generate_card()
                    if card in Poker.hand.values():
                        continue
                    else:
                        Poker.hand[int(key)] = card
                        break

class UserInput:
    """
    On the press of a key, take actions based on which key is pressed
    param key : key is the key pressed
    var out : str is a formatted dicitonary of held cards
    """
    def on_press(key):
        try:
            out = ''
            if str(key) == 'Key.enter':
                print(" "*60,"\n")
                os.system('clear')
                Poker.modify_hand()
                Poker.format_hand(Poker.hand)
                Poker.determine_match()
                print("Holding:",end=" ")
                for key, value in Poker.held.items():
                    out += f"[{key}]: {value}  "
                print(out.rstrip(),end='\r')

            # On Delete reset the terminal settings, clear the echo buffer, and exit
            elif str(key) == 'Key.delete':
                os.system('clear')
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, original_settings)
                print("Exiting Game...")
                time.sleep(0.5)
                tty.setcbreak(sys.stdin.fileno())
                os.killpg(os.getpgid(os.getpid()), signal.SIGTSTP)

            # Keys 1-5 handle the hand being held
            elif str(key.char) in ['1', '2', '3', '4', '5']:
                # Hold the card
                if Poker.IO.get(int(key.char)) == 0:
                    Poker.IO[int(key.char)] = 1
                    if Poker.hand[int(key.char)] not in Poker.held:
                        Poker.held[int(key.char)] = Poker.hand[int(key.char)]
                    else:
                        pass
                    print(" "*60, end="\r")
                    print("Holding:",end=" ")
                    for key, value in Poker.held.items():
                        out += f"[{key}]: {value}  "
                    print(out.rstrip(),end='\r')
                # Release the card
                elif Poker.IO.get(int(key.char)) == 1:
                    Poker.IO[int(key.char)] = 0
                    Poker.held[int(key.char)] = ''
                    print(" "*60, end="\r")
                    print("Holding:",end=" ")
                    for key, value in Poker.held.items():
                        out += f"[{key}]: {value}  "
                    print(out.rstrip(),end='\r')
        except:
            pass

    """
    Listens for keystrokes
    """
    def listen():
        with keyboard.Listener(on_press=UserInput.on_press) as listener:
            listener.join()

Poker = Poker()

"""
Main Function
"""
def __main__():
    os.system('clear')
    Poker.format_hand(Poker.hand)
    try:
        UserInput.listen()
    except:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, original_settings)
        exit()

if __name__ == "__main__":
    __main__()
