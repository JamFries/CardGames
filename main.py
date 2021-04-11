from Deck import Deck
from Player import Player
from Blackjack import Blackjack

import pygame

pygame.init() #Initialize pygame
screenWidth = 800
screenHeight = 600

screen = pygame.display.set_mode((screenWidth, screenHeight)) #Create the pygame screen object

whiteColor = (255, 255, 255)
greenColor = (0, 128, 0)

color_buttonLight = (170, 170, 170)
color_buttonDark = (100, 100, 100)

width = screen.get_width()
height = screen.get_height()

smallFont = pygame.font.SysFont('Arial', 35)
text = smallFont.render('Quit', True, whiteColor)

running = True

while (running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pass



########################################################################################################################
#Standard Deck
# suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
# rankings = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] # Ace(Low) -> King
# deckStandard = Deck(suits, rankings)
#
# # deckStandard.shuffle()
# # deckStandard.show()
#
#
# p1 = Player("JamFries")
# p2 = Player("Guest")
#
# b1 = Blackjack(deckStandard)
# b1.startGame([p1, p2])
########################################################################################################################
