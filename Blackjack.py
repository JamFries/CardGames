from Player import Player
from Deck import Deck
from Card import Card
import copy

# Implement Blackjack (https://bicyclecards.com/how-to-play/blackjack/)
class Blackjack:
    def __init__(self, deck):
        self.deck = deck
        self.players = []
        self.actionablePlayers = []

        self.initSuits = deck.suits
        self.initRanks = deck.ranks

    def startGame(self, players):
        self.deck = self.createNewDeck(self.initSuits, self.initRanks) # Creates a brand new deck to play each round
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

        # Create a list of players that have 'actions' (excludes dealer/people that stand)
        self.actionablePlayers = self.players.copy() #Use list.copy() to actually copy data in memory
        self.actionablePlayers.pop() # Remove the dealer from this because they go after all players bust/stand

        for player in self.actionablePlayers:
            self.calculateScore(player)
            self.showScore(player)

        # Get input from player on what the next thing to do is
        while (len(self.actionablePlayers) > 0):
            for player in self.actionablePlayers:
                print(str(player.username) + ", it is your turn")

                # Included this after because you play till stand/bust, not take turns
                lengthOfActionablePlayers = len(self.actionablePlayers)
                while (len(self.actionablePlayers) == lengthOfActionablePlayers):

                    for card in player.cards:
                        print(card.showAsString())

                    print("Type 'hit' or 'stand'")  # temporary implementation until gui
                    userInput = input()
                    if userInput == "hit":
                        self.hit(player)
                    elif userInput == "stand":
                        self.stand(player)
                    else:
                        print("Wrong input, id normally account for this but its gonna be replaced by gui anyway")

        # After all players have busted or chose stand
        dealer = self.players[len(self.players) - 1]
        self.performDealerActions(dealer)

        # After all game moves have finished, compare scores to see who won
        results = self.determineWinners(self.players)
        for playerTuple in results:
            p, score, result = playerTuple
            if (result == 'w'):
                print(str(p.username) + " won with a score of " + str(score))
            elif (result == 't'):
                print(str(p.username) + " tied with a score of " + str(score))

        # Prompt to play again
        replayers = self.promptPlayersToPlayAgain()
        if (len(replayers) > 0):
            self.startGame(replayers) # Run it back with the replayers

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
        card.Hidden = False
        player.cards.append(card)

        print(card.showAsString())

        self.calculateScore(player)
        self.showScore(player)

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
        dealer.cards[-1].Hidden = False # The dealer reveals their second card
        self.calculateScore(dealer)
        self.showScore(dealer)
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
            winners.append((players[len(players) - 1], dealerScore), 'w') # The dealer won

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
