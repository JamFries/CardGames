from Player import Player
from Deck import Deck
from Card import Card
import copy

import pygame

# Implement Blackjack (https://bicyclecards.com/how-to-play/blackjack/)
class BlackjackForGUI:
    def __init__(self, deck, screen):
        self.deck = deck
        self.players = []
        self.actionablePlayers = []

        self.screen = screen # needs access to the screen(from pygame) to draw on

        self.initSuits = deck.suits
        self.initRanks = deck.ranks

    def startGame(self, players):
        self.deck = self.createNewDeck(self.initSuits, self.initRanks) # Creates a brand new deck to play each round

        # Reset the player cards/scores for each playthrough
        for player in players:
            player.cards = []
            player.gameScore_One = 0
            player.gameScore_Two = 0

        print("Blackjack Game Begin")

        self.players = players #Get the list of players
        theDealer = Player("Dealer")
        theDealer.isDealer = True
        self.players.append(theDealer)
        for player in self.players:
            player.resetGameScore()

        self.deck.shuffle() #Shuffle the deck
        print("Deck Size: " + str(len(self.deck.cards)))
        print("Deck Shuffled")

        self.initialDeal() # Deal cards to each player
        # draw rectangles (cards) for each player after they have been dealt
        self.drawPlayerCards(self.screen)
        pygame.display.update()


        # Create a list of players that have 'actions' (excludes dealer/people that stand)
        self.actionablePlayers = self.players.copy() #Use list.copy() to actually copy data in memory
        self.actionablePlayers.pop() # Remove the dealer from this because they go after all players bust/stand

        for player in self.actionablePlayers:
            self.calculateScore(player)
            self.showScore(player)

        self.drawPlayerScore() #Draws text on score of each player's score
        pygame.display.update()

        # Get input from player on what the next thing to do is
        while (len(self.actionablePlayers) > 0):
            for player in self.actionablePlayers:
                print(str(player.username) + ", it is your turn")

                # Included this after because you play till stand/bust, not take turns
                lengthOfActionablePlayers = len(self.actionablePlayers)
                while (len(self.actionablePlayers) == lengthOfActionablePlayers):

                    # Draw buttons for hit and stand
                    hitRect = self.drawHitButton()
                    standRect = self.drawStandButton()
                    pygame.display.update()

                    # for card in player.cards:
                    #    print(card.showAsString())

                    # print("Type 'hit' or 'stand'")  # temporary implementation until gui

                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                if (hitRect.collidepoint(event.pos)):
                                    print("Hit was clicked")
                                    self.hit(player)
                                    pygame.display.update()
                                elif (standRect.collidepoint(event.pos)):
                                    print("Stand was clicked")
                                    self.stand(player)
                                    pygame.display.update()

        # After all players have busted or chose stand
        dealer = self.players[len(self.players) - 1]
        self.performDealerActions(dealer) # !pygame stuff was put in here!

        # After all game moves have finished, compare scores to see who won
        results = self.determineWinners(self.players)

        self.drawResults(results)
        pygame.display.update()


        playAgainRect = self.drawPlayAgainButton()
        exitRect = self.drawExitButton()
        pygame.display.update()

        self.resetAllStats() #Reset all important information before beginning another round or not

        while(1): # This will loop until the user selects either play again or exit
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if (playAgainRect.collidepoint(event.pos)):
                            print("Play Again was clicked")
                            pygame.display.update()
                            return True # return true to play again
                        elif (exitRect.collidepoint(event.pos)):
                            print("Exit was clicked")
                            pygame.display.update()
                            return False
            self.drawPlayAgainButton()
            self.drawExitButton()
            pygame.display.update() #called here to keep updating the button shading based on mouse position

        # for playerTuple in results:
        #     p, score, result = playerTuple
        #     if (result == 'w'):
        #         print(str(p.username) + " won with a score of " + str(score))
        #
        #     elif (result == 't'):
        #         print(str(p.username) + " tied with a score of " + str(score))

        # Prompt to play again
        # replayers = self.promptPlayersToPlayAgain()

        # if (len(replayers) > 0):
        #     self.startGame(replayers) # Run it back with the replayers

    # Function does the initial deal in blackjack: 2 rounds around the table with 1 card face-down for the dealer
    def initialDeal(self):
        for i in range(0, 2, 1):
            for j in range(0, len(self.players), 1):
                if ((i == 1) and (j == len(self.players) - 1)): # Check if its the last card for the dealer
                    card = self.deck.dealCard()
                    card.Hidden = True # The second card for the dealer stays hidden
                    self.players[j].cards.append(card)
                else:
                    card = self.deck.dealCard()
                    card.hidden = False
                    self.players[j].cards.append(card)
                    # print("Player " + str(j) + " was dealt: " + card.showAsString())

    # Function that takes a player's hand and determines the score of that hand
    def calculateScore(self, player):
        # Need to reset because we call this in multiple locations
        player.gameScore_One = 0
        player.gameScore_Two = 0

        for card in player.cards:
            if (card.rank == 1): # Deal with the ace separately
                player.gameScore_One += 1
                player.gameScore_Two += 11
            else:
                player.gameScore_One += self.cardToScore(card)
                player.gameScore_Two += self.cardToScore(card)

    # Function to give another card from the deck to the player
    def hit(self, player):
        print("The player chose hit")
        card = self.deck.dealCard()
        card.hidden = False
        player.cards.append(card)

        print(card.showAsString())
        self.drawPlayerCards(self.screen)

        self.calculateScore(player)
        self.showScore(player)

        # quick-fix way to fix the fact that we arent screen.fill()-ing back in main because of b1.startGame() happening
        self.screen.fill((0, 128, 0)) # Erase the contents drawn on screen
        # Then redraw everything up to this point
        self.drawPlayerCards(self.screen)
        self.drawPlayerScore()
        pygame.display.update()

        if (player.gameScore_One > 21 and player.gameScore_Two > 21): # The player busted
            try:
                self.actionablePlayers.remove(player)
            except ValueError: #This will happen when the dealer calls this to hit and busts
                print("The dealer busted")

    # Function to remove that player from the list of players still performing actions
    def stand(self, player):
        print("The player chose stand")
        try:
            self.actionablePlayers.remove(player) # Removes player from the list of actionable players
        except ValueError:
            pass # print("The dealer chose stand")

    # Function to play the dealer's hand until they stand or bust
    def performDealerActions(self, dealer):
        print("The dealer is now performing their actions")
        dealer.cards[-1].hidden = False # The dealer reveals their second card
        self.calculateScore(dealer)
        self.showScore(dealer)

        # quick-fix way to fix the fact that we arent screen.fill()-ing back in main because of b1.startGame() happening
        self.screen.fill((0, 128, 0))
        self.drawPlayerCards(self.screen)
        self.drawPlayerScore()
        pygame.display.update()

        for card in dealer.cards:
            print(card.showAsString())

        while(dealer.gameScore_One < 17):
            wonGame = self.dealerActionCheckWinBefore17(self.players)
            if (wonGame):
                self.stand(dealer)  # Stand at whatever number because they already surpassed the players
                break

            if (dealer.gameScore_One == dealer.gameScore_Two): # No double calculations
                self.hit(dealer)
            elif (dealer.gameScore_One > 21 and dealer.gameScore_Two < 17):
                self.hit(dealer)
            elif (dealer.gameScore_One < 17 and dealer.gameScore_Two > 21):
                self.hit(dealer)
            elif (dealer.gameScore_One < 17 and dealer.gameScore_Two < 17):
                self.hit(dealer)
            else:
                self.stand(dealer)

    # Function to determine the winners of the round
    # (this could be cleaned up alot, i forgot everyone plays against the dealer only and not each other)
    def determineWinners(self, players):
        winners = []
        tieExists = False

        dealerScore = self.determineBestScore(players[len(players) - 1]) #Get dealers best score
        for i in range(0, len(players) - 1):
            playerScore = self.determineBestScore(players[i])
            if dealerScore == -1: # The dealer busted, every player that didnt bust wins
                if playerScore != -1:
                    winners.append((players[i], playerScore, 'w'))
            else: # The dealer did not bust, every player greater their score wins and equal their score ties
                if (playerScore == dealerScore):
                    winners.append((players[i], playerScore, 't'))
                    tieExists = True # Meaning we add dealer to 'winners' list at the end
                elif (playerScore > dealerScore):
                    winners.append((players[i], playerScore, 'w'))

        if tieExists:
            winners.append((players[len(players) - 1], dealerScore, 't')) # A tie only exists with the dealer so add them

        if (len(winners) == 0): # If the list is empty by this point, it means the dealer had the highest value of all
            winners.append((players[len(players) - 1], dealerScore, 'w')) # The dealer won

        return winners # Return list of tuples (player, int, char)


    def determineDealerScore(self, dealer):
        blackjackScore_One = 21 - dealer.gameScore_One
        blackjackScore_Two = 21 - dealer.gameScore_Two
        blackjackScore = 999  # both busts

        if (blackjackScore_One >= 0 and blackjackScore_Two >= 0):  # no busts
            blackjackScore = min(blackjackScore_One, blackjackScore_Two)
        elif (blackjackScore_One >= 0 and blackjackScore_Two < 0):  # one bust (ace calculation)
            blackjackScore = blackjackScore_One
        elif (blackjackScore_One < 0 and blackjackScore_Two >= 0):  # one bust (ace calculation)
            blackjackScore = blackjackScore_Two

        return blackjackScore

    # Function for the dealer to automatically stand if they beat all players even though they are not at 17 yet
    def dealerActionCheckWinBefore17(self, players):
        dealerTopScore = self.determineBestScore(players[len(players) - 1]) # determine best score for dealer
        for i in range(0, len(players) - 1, 1): #excludes dealer in search
            playerTopScore = self.determineBestScore(players[i])
            if (playerTopScore > dealerTopScore and dealerTopScore < 17):
                return False
        return True

    def showScore(self, player):
        if (player.gameScore_One != player.gameScore_Two):
            print(str(player.username) + " Score: " + str(player.gameScore_One) + " / " + str(player.gameScore_Two))
        else:
            print(str(player.username) + " Score: " + str(player.gameScore_One))

    # Function to easily convert a card to a score in blackjack (except Ace)
    def cardToScore(self, card):
        if (card.rank == 2):
            return 2
        elif (card.rank == 3):
            return 3
        elif (card.rank == 4):
            return 4
        elif (card.rank == 5):
            return 5
        elif (card.rank == 6):
            return 6
        elif (card.rank == 7):
            return 7
        elif (card.rank == 8):
            return 8
        elif (card.rank == 9):
            return 9
        elif (card.rank == 10):
            return 10
        elif(card.rank == 11):
            return 10
        elif(card.rank == 12):
            return 10
        elif(card.rank == 13):
            return 10

    # Not fully implemented best score finder for player
    def determineBestScore(self, player):
        score1 = player.gameScore_One
        score2 = player.gameScore_Two

        if (score1 > 21 and score2 > 21):
            return -1
        elif (score1 > 21):
            return score2
        elif (score2 > 21):
            return score1
        elif (score1 > score2):
            return score1
        else:
            return score2

    def promptPlayersToPlayAgain(self):
        replayers = []
        for i in range(0, len(self.players) - 1, 1):
            print(str(self.players[i].username) + ", would you like to play again?\n")
            print("Type 'Yes' or 'No'")
            response = input()
            while (response != 'Yes' and response != 'No'):
                print("Invalid Response\n")
                print("Type 'Yes' or 'No'")
                response = input()
            if (response == 'Yes'):
                replayers.append(self.players[i])
            else:
                print("See you later, " + str(self.players[i].username))

        return replayers

    # Function to create a fresh deck based on the suits/ranks that were from the deck passed through to the game
    # (idk exactly how python memory works this might cause memory problems)
    # (if so then manually delete old decks before creating new ones but for now w/e)
    def createNewDeck(self, suits, ranks):
        retVal = Deck(suits, ranks)
        return retVal


    def drawPlayerCards(self, screen):
        #Draw cards in different locations depending on playerCount
        if (len(self.players) == 2): # 1 player + dealer
            width = screen.get_width()
            height = screen.get_height()

            cardWidth = 80
            cardHeight = 140

            # pygame rect() structure: left, top, width, height
            cardLeft = (width / 2)  # middle of screen
            cardTop = height - (height / 5)  # near the bottom

            for player in self.players:
                if player != self.players[len(self.players) - 1]: # If there not the dealer
                    smallFont = pygame.font.SysFont('Arial', 24)

                    for card in player.cards:
                        cardImg = self.getCardAsSprite(card) # Get the image for the specific card
                        screen.blit(cardImg, (cardLeft, cardTop))
                        cardLeft += cardWidth

                        # cardName = card.showAsString()
                        # text = smallFont.render(cardName, True, (255, 255, 255))
                        # textRect = text.get_rect(center=(cardLeft + (cardWidth / 2), cardTop + (cardHeight / 2)))  # textRect to center the text within the pygame.rect drawn
                        #
                        # pygame.draw.rect(screen, (100, 100, 100), [cardLeft, cardTop, cardWidth, cardHeight])
                        # screen.blit(text, textRect)
                        # cardLeft += cardWidth # Move the place to draw next card over by the width of one card
                else:
                    #Draw the dealer cards now
                    cardLeft = (width / 2) # center the dealer
                    cardTop = (height / 10) # dealer cards are at top of screen

                    # smallFont = pygame.font.SysFont('Arial', 24)

                    for card in player.cards:
                        cardImg = self.getCardAsSprite(card)
                        screen.blit(cardImg, (cardLeft, cardTop))
                        cardLeft += cardWidth

                        # if card.hidden == False:
                        #     cardName = card.showAsString()
                        #
                        #     text = smallFont.render(cardName, True, (255, 255, 255))
                        #     textRect = text.get_rect(center=(cardLeft + (cardWidth / 2), cardTop + (cardHeight / 2)))  # textRect to center the text within the pygame.rect drawn
                        #     pygame.draw.rect(screen, (100, 100, 100), [cardLeft, cardTop, cardWidth, cardHeight])
                        #     screen.blit(text, textRect)
                        # else:
                        #     pygame.draw.rect(screen, (100, 100, 100), [cardLeft, cardTop, cardWidth, cardHeight])
                        # cardLeft += cardWidth  # Move the place to draw next card over by the width of one card


    # Function that will take a card and return its sprite form to be used for the pygame window
    def getCardAsSprite(self, card):
        imgString = "images/"

        if (card.hidden == True):
            imgString += "Card-Back.png"
            return pygame.image.load(imgString) # Hide the dealer's second card until its time to reveal it

        if (card.rank == 1):
            imgString += "Ace"
        elif (card.rank == 2):
            imgString += "Two"
        elif (card.rank == 3):
            imgString += "Three"
        elif (card.rank == 4):
            imgString += "Four"
        elif (card.rank == 5):
            imgString += "Five"
        elif (card.rank == 6):
            imgString += "Six"
        elif (card.rank == 7):
            imgString += "Seven"
        elif (card.rank == 8):
            imgString += "Eight"
        elif (card.rank == 9):
            imgString += "Nine"
        elif (card.rank == 10):
            imgString += "Ten"
        elif (card.rank == 11):
            imgString += "Jack"
        elif (card.rank == 12):
            imgString += "Queen"
        elif (card.rank == 13):
            imgString += "King"

        if (card.suit == "Diamonds"):
            imgString += "-D"
        elif (card.suit == "Hearts"):
            imgString += "-H"
        elif (card.suit == "Clubs"):
            imgString += "-C"
        elif (card.suit == "Spades"):
            imgString += "-S"

        imgString += ".png"

        return pygame.image.load(imgString) # Return the pygame image loaded from the card's corresponding image

    def drawPlayerScore(self):
        if (len(self.players) == 2): # 1 player + dealer
            width = self.screen.get_width()
            height = self.screen.get_height()
            font = pygame.font.SysFont('Arial', 24)


            for player in self.players:
                if (player != self.players[len(self.players) - 1]): # If not the dealer
                    playerOneScoreWidth = (width / 2) - 30
                    playerOneScoreHeight = height - (height / 5) - 30

                    if (player.gameScore_One == player.gameScore_Two):
                        text = str(player.gameScore_One)
                        scoreText = font.render(text, True, (255, 255, 255))
                        self.screen.blit(scoreText, (playerOneScoreWidth, playerOneScoreHeight))
                    else:
                        text = str(player.gameScore_One) + " / " + str(player.gameScore_Two)
                        scoreText = font.render(text, True, (255, 255, 255))
                        self.screen.blit(scoreText, (playerOneScoreWidth, playerOneScoreHeight))
                else: # Dealer score
                    if (player.gameScore_One == 0): # Means this part of the game the card is hidden, dont draw for now
                        pass
                    else:
                        if (player.gameScore_One == player.gameScore_Two):
                            text = str(player.gameScore_One)
                            scoreText = font.render(text, True, (255, 255, 255))
                            self.screen.blit(scoreText,
                                             ((width / 2) - 20, height / 10))  # -20 to width to make it close to cards
                        else:
                            text = str(player.gameScore_One) + " / " + str(player.gameScore_Two)
                            scoreText = font.render(text, True, (255, 255, 255))
                            self.screen.blit(scoreText,
                                             ((width / 2) - 20, height / 10))  # -20 to width to make it close to cards


    def drawHitButton(self):
        width = self.screen.get_width()
        height = self.screen.get_height()

        buttonWidth = 140
        buttonHeight = 40

        # pygame rect() structure: left, top, width, height
        buttonLeft = (width / 20)
        buttonTop = (height / 2)

        smallFont = pygame.font.SysFont('Arial', 35)
        text = smallFont.render('Hit', True, (255, 255, 255))
        textRect = text.get_rect(center=(buttonLeft + (buttonWidth/2), buttonTop + (buttonHeight/2))) #textRect to center the text within the pygame.rect drawn

        mouse = pygame.mouse.get_pos()  # mouse[0] is mouse.x, mouse[1] is mouse.y

        if ((buttonLeft <= mouse[0] <= (buttonLeft + buttonWidth)) and (buttonTop <= mouse[1] <= (buttonTop + buttonHeight))):
            pygame.draw.rect(self.screen, (170, 170, 170), [buttonLeft, buttonTop, buttonWidth, buttonHeight])
        else:
            pygame.draw.rect(self.screen, (100, 100, 100), [buttonLeft, buttonTop, buttonWidth, buttonHeight])

        self.screen.blit(text, textRect)

        return pygame.Rect(buttonLeft, buttonTop, buttonWidth, buttonHeight)

    def drawStandButton(self):
        width = self.screen.get_width()
        height = self.screen.get_height()

        buttonWidth = 140
        buttonHeight = 40

        # pygame rect() structure: left, top, width, height
        buttonLeft = width - (width / 20) - buttonWidth
        buttonTop = (height / 2)

        smallFont = pygame.font.SysFont('Arial', 35)
        text = smallFont.render('Stand', True, (255, 255, 255))
        textRect = text.get_rect(center=(buttonLeft + (buttonWidth/2), buttonTop + (buttonHeight/2))) #textRect to center the text within the pygame.rect drawn

        mouse = pygame.mouse.get_pos()  # mouse[0] is mouse.x, mouse[1] is mouse.y

        if ((buttonLeft <= mouse[0] <= (buttonLeft + buttonWidth)) and (buttonTop <= mouse[1] <= (buttonTop + buttonHeight))):
            pygame.draw.rect(self.screen, (170, 170, 170), [buttonLeft, buttonTop, buttonWidth, buttonHeight])
        else:
            pygame.draw.rect(self.screen, (100, 100, 100), [buttonLeft, buttonTop, buttonWidth, buttonHeight])

        self.screen.blit(text, textRect)

        return pygame.Rect(buttonLeft, buttonTop, buttonWidth, buttonHeight)

    def drawResults(self, results):
        font = pygame.font.SysFont("Arial", 35)
        width = self.screen.get_width()
        height = self.screen.get_height()

        endGameTextWidth = (width / 2)
        endGameTextHeight = (height / 4)

        for playerTuple in results:
            p, score, result = playerTuple
            if (result == 'w'):
                # print(str(p.username) + " won with a score of " + str(score))
                winString = str(p.username) + " won with a score of " + str(score)
                winText = font.render(winString, True, (255, 255, 255))

                self.screen.blit(winText, (endGameTextWidth, endGameTextHeight))
                endGameTextHeight += ((height) - (height / 10)) # to separate lines of text
            elif (result == 't'):
                # print(str(p.username) + " tied with a score of " + str(score))
                tieString = str(p.username) + " tied with a score of " + str(score)
                tieText = font.render(tieString, True, (255, 255, 255))

                self.screen.blit(tieText, (endGameTextWidth, endGameTextHeight))
                endGameTextHeight += ((height) - (height / 10))

    def drawPlayAgainButton(self):
        width = self.screen.get_width()
        height = self.screen.get_height()

        buttonWidth = 140
        buttonHeight = 40

        # pygame rect() structure: left, top, width, height
        buttonLeft = (width / 20)
        buttonTop = (height / 2)

        smallFont = pygame.font.SysFont('Arial', 35)
        text = smallFont.render('Play Again', True, (255, 255, 255))
        textRect = text.get_rect(center=(buttonLeft + (buttonWidth/2), buttonTop + (buttonHeight/2))) #textRect to center the text within the pygame.rect drawn

        mouse = pygame.mouse.get_pos()  # mouse[0] is mouse.x, mouse[1] is mouse.y

        if ((buttonLeft <= mouse[0] <= (buttonLeft + buttonWidth)) and (buttonTop <= mouse[1] <= (buttonTop + buttonHeight))):
            pygame.draw.rect(self.screen, (170, 170, 170), [buttonLeft, buttonTop, buttonWidth, buttonHeight])
        else:
            pygame.draw.rect(self.screen, (100, 100, 100), [buttonLeft, buttonTop, buttonWidth, buttonHeight])

        self.screen.blit(text, textRect)

        return pygame.Rect(buttonLeft, buttonTop, buttonWidth, buttonHeight)

    def drawExitButton(self):
        width = self.screen.get_width()
        height = self.screen.get_height()

        buttonWidth = 140
        buttonHeight = 40

        # pygame rect() structure: left, top, width, height
        buttonLeft = width - (width / 20) - buttonWidth
        buttonTop = (height / 2)

        smallFont = pygame.font.SysFont('Arial', 35)
        text = smallFont.render('Exit', True, (255, 255, 255))
        textRect = text.get_rect(center=(buttonLeft + (buttonWidth/2), buttonTop + (buttonHeight/2))) #textRect to center the text within the pygame.rect drawn

        mouse = pygame.mouse.get_pos()  # mouse[0] is mouse.x, mouse[1] is mouse.y

        if ((buttonLeft <= mouse[0] <= (buttonLeft + buttonWidth)) and (buttonTop <= mouse[1] <= (buttonTop + buttonHeight))):
            pygame.draw.rect(self.screen, (170, 170, 170), [buttonLeft, buttonTop, buttonWidth, buttonHeight])
        else:
            pygame.draw.rect(self.screen, (100, 100, 100), [buttonLeft, buttonTop, buttonWidth, buttonHeight])

        self.screen.blit(text, textRect)

        return pygame.Rect(buttonLeft, buttonTop, buttonWidth, buttonHeight)


    def resetAllStats(self):
        for player in self.players:
            player.gameScore_One = 0
            player.gameScore_Two = 0
            player.cards = []
        self.actionablePlayers = []