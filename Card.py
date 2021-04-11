class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.hidden = True

    def showAsString(self):
        return str(self.rank) + " of " + str(self.suit)