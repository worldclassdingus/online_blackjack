import random

# file for the deck and cards


# card ranks and suits
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['♠︎', '♥︎', '♣︎', '♦︎']

# map ranks to their values
RANK_VALUES = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 10,
    'Q': 10,
    'K': 10,
    'A': 1
}

# card class
# stores a rank, suit and value
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = RANK_VALUES.get(rank)

    # override the string function to return the rank and suit
    def __str__(self):
        return f'{self.rank}{self.suit}'

# deck class
# contains a shuffled list of playing cards
class Deck:
    def __init__(self):

        self.cards = []

        # add a card for every rank and suit
        for rank in RANKS:
            for suit in SUITS:
                self.cards.append(Card(rank, suit))
        
        # shuffle the deck
        random.shuffle(self.cards)
    
    # deal cards from the deck
    # returns a list of Cards
    def deal(self, n):
        cards_dealt = []

        for i in range(n):
            cards_dealt.append(self.cards.pop())
        
        return cards_dealt