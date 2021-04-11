import random
from Card import Card

class Deck:
    def __init__(self, suits, ranks):
        self.cards = []

        self.suits = suits
        self.ranks = ranks

        for i in suits:
            for j in ranks:
                self.cards.append(Card(i, j))

    def showAsString(self): # Print the entire deck
        for i in self.cards:
            return i.showAsString() + ", "

    # Fisher-Yates Shuffle Algorithm (https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle#The_modern_algorithm)
    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            j = random.randint(0, i)
            temp = self.cards[j]
            self.cards[j] = self.cards[i]
            self.cards[i] = temp

    # Function that removes and returns the card off of the 'top' of the deck
    def dealCard(self):
        card = self.cards.pop()
        return card
