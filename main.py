from Deck import Deck
from Player import Player
from Blackjack import Blackjack
from BlackjackForGUI import BlackjackForGUI

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


gameState = 0 # Track what to draw on the pygame screen depending on user action
# 0: draw the blackjack menu
# 1: draw the playerCount menu
# 2: draw the blackjack game

# Helper function to make a deck of cards
def createStandardDeck():
    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rankings = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] # Ace(Low) -> King
    deck = Deck(suits, rankings)
    return deck

# Function to draw the play button onto the screen of the pygame window
def drawPlayButton(screen):
    width = screen.get_width()
    height = screen.get_height()

    buttonWidth = 140
    buttonHeight = 40

    # pygame rect() structure: left, top, width, height
    buttonLeft = (width / 2) - (buttonWidth / 2)  # (buttonWidth / 2) so the button does not start at the middle, but instead is centered
    buttonTop = (height / 4) # The top 1/4 of the screen

    smallFont = pygame.font.SysFont('Arial', 35)
    text = smallFont.render('Play', True, whiteColor)

    mouse = pygame.mouse.get_pos()  # mouse[0] is mouse.x, mouse[1] is mouse.y

    if ((buttonLeft <= mouse[0] <= (buttonLeft + buttonWidth)) and (buttonTop <= mouse[1] <= (buttonTop + buttonHeight))):
        pygame.draw.rect(screen, color_buttonLight, [buttonLeft, buttonTop, buttonWidth, buttonHeight])
    else:
        pygame.draw.rect(screen, color_buttonDark, [buttonLeft, buttonTop, buttonWidth, buttonHeight])

    screen.blit(text, (buttonLeft + (buttonWidth / 4), buttonTop))  # Draw the text onto the screen (positioned on button)

    return pygame.Rect(buttonLeft, buttonTop, buttonWidth, buttonHeight) #Return the rect area where the button is

# Function to draw the play button onto the screen of the pygame window
def drawQuitButton(screen):
    width = screen.get_width()
    height = screen.get_height()

    buttonWidth = 140
    buttonHeight = 40

    # pygame rect() structure: left, top, width, height
    buttonLeft = (width / 2) - (buttonWidth / 2)  # (buttonWidth / 2) so the button does not start at the middle, but instead is centered
    buttonTop = height - (height / 4)  # The bottom 1/4 of the screen

    smallFont = pygame.font.SysFont('Arial', 35)
    text = smallFont.render('Quit', True, whiteColor)

    mouse = pygame.mouse.get_pos()  # mouse[0] is mouse.x, mouse[1] is mouse.y

    if ((buttonLeft <= mouse[0] <= (buttonLeft + buttonWidth)) and (buttonTop <= mouse[1] <= (buttonTop + buttonHeight))):
        pygame.draw.rect(screen, color_buttonLight, [buttonLeft, buttonTop, buttonWidth, buttonHeight])
    else:
        pygame.draw.rect(screen, color_buttonDark, [buttonLeft, buttonTop, buttonWidth, buttonHeight])

    screen.blit(text, (buttonLeft + (buttonWidth / 4), buttonTop))  # Draw the text onto the screen (positioned on button)

    return pygame.Rect(buttonLeft, buttonTop, buttonWidth, buttonHeight)

# Function to draw the title onto the pygame screen
def drawTitle(screen):
    width = screen.get_width()
    height = screen.get_height()

    font = pygame.font.SysFont('Arial', 42)
    text = font.render('Blackjack', True, (0, 0, 0))
    textRect = text.get_rect(center=(width / 2, height / 6)) # Center the text-rectangle created by the text

    screen.blit(text, textRect)

def drawOnePlayerButton(screen):
    width = screen.get_width()
    height = screen.get_height()

    buttonWidth = 140
    buttonHeight = 40

    # pygame rect() structure: left, top, width, height
    buttonLeft = (width / 2) - (buttonWidth / 2)  # (buttonWidth / 2) so the button does not start at the middle, but instead is centered
    buttonTop = (height / 4)  # The bottom 1/4 of the screen

    smallFont = pygame.font.SysFont('Arial', 35)
    text = smallFont.render('1 Player', True, whiteColor)
    textRect = text.get_rect(center=(buttonLeft + (buttonWidth/2), buttonTop + (buttonHeight/2))) #textRect to center the text within the pygame.rect drawn

    mouse = pygame.mouse.get_pos()  # mouse[0] is mouse.x, mouse[1] is mouse.y

    if ((buttonLeft <= mouse[0] <= (buttonLeft + buttonWidth)) and (buttonTop <= mouse[1] <= (buttonTop + buttonHeight))):
        pygame.draw.rect(screen, color_buttonLight, [buttonLeft, buttonTop, buttonWidth, buttonHeight])
    else:
        pygame.draw.rect(screen, color_buttonDark, [buttonLeft, buttonTop, buttonWidth, buttonHeight])

    # screen.blit(text, (buttonLeft + (buttonWidth / 4), buttonTop))  # Draw the text onto the screen (positioned on button)
    screen.blit(text, textRect)

    return pygame.Rect(buttonLeft, buttonTop, buttonWidth, buttonHeight)

def drawBeginButton(screen):
    width = screen.get_width()
    height = screen.get_height()

    buttonWidth = 140
    buttonHeight = 40

    # pygame rect() structure: left, top, width, height
    buttonLeft = (width / 20)
    buttonTop = (height / 10)

    smallFont = pygame.font.SysFont('Arial', 35)
    text = smallFont.render('Begin', True, whiteColor)
    textRect = text.get_rect(center=(buttonLeft + (buttonWidth/2), buttonTop + (buttonHeight/2))) #textRect to center the text within the pygame.rect drawn

    mouse = pygame.mouse.get_pos()  # mouse[0] is mouse.x, mouse[1] is mouse.y

    if ((buttonLeft <= mouse[0] <= (buttonLeft + buttonWidth)) and (buttonTop <= mouse[1] <= (buttonTop + buttonHeight))):
        pygame.draw.rect(screen, color_buttonLight, [buttonLeft, buttonTop, buttonWidth, buttonHeight])
    else:
        pygame.draw.rect(screen, color_buttonDark, [buttonLeft, buttonTop, buttonWidth, buttonHeight])

    screen.blit(text, textRect)

    return pygame.Rect(buttonLeft, buttonTop, buttonWidth, buttonHeight)

running = True
while (running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # LMB clicked
                # Determine what to check for based on gameState
                if (gameState == 0):
                    #Check if menu elements were clicked
                    if playRect.collidepoint(event.pos):
                        print("Play was clicked")
                        gameState = 1
                    elif quitRect.collidepoint(event.pos):
                        print("Quit was clicked")
                        running = False
                elif (gameState == 1):
                    #Check if playerCount elements were clicked
                    if onePlayerRect.collidepoint(event.pos):
                        print("1 Player was clicked")
                        gameState = 2 # Set the next gameState
                        deck = createStandardDeck() # Make a deck of cards for the game
                        p1 = Player("Player 1") # Make one player
                        b1 = BlackjackForGUI(deck) # Make a blackjack instance
                        b1.startGame([p1]) # Start the game with the number of players




    screen.fill(greenColor) # Fill the background

    # Draw the content on the screen depending on the gameState
    if (gameState == 0): # Blackjack Menu screen
        # Draw the elements of the menu
        drawTitle(screen)
        playRect = drawPlayButton(screen)
        quitRect = drawQuitButton(screen)

    elif (gameState == 1): # Player Count screen
        # Draw the elements of the menu
        drawTitle(screen)
        onePlayerRect = drawOnePlayerButton(screen)

    elif (gameState == 2): # Blackjack Game screen
        beginRect = drawBeginButton(screen)

    pygame.display.update()





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
