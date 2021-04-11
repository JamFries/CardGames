from Card import Card

class Player:
    def __init__(self, username="player"):
        self.username = username
        self.chips = 0
        self.cards = []
        self.isDealer = False
        self.gameScore_One = 0
        self.gameScore_Two = 0

    def resetGameScore(self):
        self.gameScore_One = 0
        self.gameScore_Two = 0

    def getChips(self):
        return self.chips

    def getCards(self):
        return self.cards