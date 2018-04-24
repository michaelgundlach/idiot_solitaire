"""
Histogram of Idiot's Solitaire outcomes.

How likely is it that a play of Idiot's Solitaire will result in 0
cards remaining?  2 cards?  4 cards? etc.
"""

def print_debug_logging(x):
    print(x)
    pass

import random

rank = lambda card: card[0]
suit = lambda card: card[1]

class Card(object):
    def __init__(self,r,s):
        self.rank=r
        self.suit=s
    def __str__(self):
        return  "%s%s" % (self.rank, self.suit)

def play(log=lambda x:0):
    """
    Play one game of solitaire.
    Return the number of cards left at the end of the game.
    """
    cards = [ Card(r,s) for r in "A23456789TJQK"
                        for s in "SHDC" ]
    random.shuffle(cards)
    up = []
    down = iter(cards)
    log( "  ".join(str(c) for c in cards) )
    try:
        while True:
            #log( "  ".join(str(c) for c in up[-4:]) )
            log( "  ".join(str(c) for c in reversed(up)))
            if len(up) >= 4 and up[-1].rank == up[-4].rank:
                log("RANK: %s" % up[-1])
                up = up[:-4] # Remove last 4
            elif len(up) >= 4 and up[-1].suit == up[-4].suit:
                log("SUIT: %s" % up[-1])
                up[-3] = up[-1] # Copy 4th to 2nd
                up = up[:-2] # Toss 3rd and (copied) 4th
            else:
                up.append(down.next())
    except StopIteration:
        return len(up)


def test():
    count = play(print_debug_logging)
    print
    print "Final count: %d" % count

def histogram(n, counts, height):
    """
    Print a histogram showing the results of |n| games of solitaire.
    |counts| is a 54-item array; counts[20] shows how many of |n|
    games ended with 20 cards left.

    |height| is the height in stars of the histogram.
    """
    percents = [0] * 54
    for i in xrange(54):
        percents[i] = counts[i] * 100.0 / n
    biggest = max(percents)
    scale = height / biggest
    stars = [x*scale for x in percents]

    for i in xrange(height + 3, -1, -1):
        char = lambda f: "*" if f > i else " "
        print " ".join(
            "%04s" % char(c) for (i,c) in enumerate(stars)
            if i % 2 == 0
            )
    print " ".join("%4d"%i for i in xrange(54) if i % 2 == 0),
    print " ::  # Cards Left"
#    print " ".join("%04.1f"%c for (i,c) in enumerate(stars) if i % 2 == 0),
#    print " ::  Star count"
    print
    print
    print " ".join("%04.1f"%c for (i,c) in enumerate(percents) if i % 2 == 0),
    print " ::  Percentage"


def main(n, height=25):
    """Play |n| games and print a |height|-height star histogram."""
    counts = [0] * 54
    for i in xrange(n):
        counts[play()] += 1
    histogram(n, counts, height)
    print "(Histogram of %d plays of Idiot's Solitaire)" % n


# Play a bunch of games and print a histogram of a certain character height,
# showing how likely you are to end with X cards
main(n=100000, height=27)
