import pygame

class BlackjackMenu:
    def __init__(self, pygameScreen):
        self.width = pygameScreen.get_width()
        self.height = pygameScreen.get_height()

        self.drawPlayButton(pygameScreen)
        self.drawPlayersButton(pygameScreen)
        self.drawExitButton(pygameScreen)

    def drawPlayButton(self, screen):
        pass # pygame.draw.rect(screen)

    def drawPlayersButton(self, screen):
        pass

    def drawExitButton(self, screen):
        pass