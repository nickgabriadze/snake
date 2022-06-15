import pygame
from random import randint as randomPos


class Apple(object):
    __appleItself = pygame.transform.scale(pygame.image.load("SnakeAssets/SnakeApple.png"), (40, 40))

    def __init__(self):
        self.apple = self.__appleItself.get_rect(topleft=[randomPos(50, 1100), randomPos(50, 500)])

    def displayApple(self, surface):
        surface.blit(self.__appleItself, (self.apple.x, self.apple.y))

    def changeApplePosition(self):
        self.apple = self.__appleItself.get_rect(topleft=[randomPos(50, 1100), randomPos(50, 500)])

    def getApple(self):
        return self.apple
