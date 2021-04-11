from Deck import Deck
from Player import Player
from Blackjack import Blackjack




########################################################################################################################
#Standard Deck
suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
rankings = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] # Ace(Low) -> King
deckStandard = Deck(suits, rankings)

# deckStandard.shuffle()
# deckStandard.show()


p1 = Player("JamFries")
p2 = Player("Guest")

b1 = Blackjack(deckStandard)
b1.startGame([p1, p2])