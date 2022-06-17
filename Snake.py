import pygame


class Snake(object):
    __mainPositionX = 300
    __mainPositionY = 300
    __direction = "RIGHT"
    __speed = 15
    __eyesUp = pygame.image.load("SnakeAssets/EyesUp.png")
    __eyesDefault = __eyesUp
    __eyesDown = pygame.image.load("SnakeAssets/EyesDown.png")

    def __init__(self):
        self.head = pygame.Rect(self.__mainPositionX, self.__mainPositionY, 30, 30)
        self.eyes = self.__eyesUp.get_rect(topleft=[self.head.x, self.head.y])
        self.body = [pygame.Rect(self.__mainPositionX - 15, self.__mainPositionY, 30, 30),
                     pygame.Rect(self.__mainPositionX - 30, self.__mainPositionY, 30, 30),
                     pygame.Rect(self.__mainPositionX - 45, self.__mainPositionY, 30, 30),
                     pygame.Rect(self.__mainPositionX - 60, self.__mainPositionY, 30, 30)]
        self.lastBlock = self.body[len(self.body) - 1]

    def displaySnake(self, surface):

        pygame.draw.rect(surface, (10, 240, 10), self.head, border_radius=7)

        for bodyPart in self.body:
            pygame.draw.rect(surface, (10, 240, 10), bodyPart, border_radius=7)
        surface.blit(self.__eyesUp, (self.head.x, self.head.y))


    def moveSnake(self):
        pressedKeys = pygame.key.get_pressed()

        if (pressedKeys[pygame.K_LEFT] or pressedKeys[pygame.K_a]) and self.__direction != "RIGHT":
            self.__direction = "LEFT"
        elif (pressedKeys[pygame.K_RIGHT] or pressedKeys[pygame.K_d]) and self.__direction != "LEFT":
            self.__direction = "RIGHT"
        elif (pressedKeys[pygame.K_DOWN] or pressedKeys[pygame.K_s]) and self.__direction != "UP":
            self.__direction = "DOWN"
        elif (pressedKeys[pygame.K_UP] or pressedKeys[pygame.K_w]) and self.__direction != "DOWN":
            self.__direction = "UP"

        if self.__direction == "RIGHT":
            self.__eyesUp = self.__eyesDefault
            self.head.x += self.__speed

        elif self.__direction == "LEFT":
            self.__eyesUp = self.__eyesDefault
            self.head.x -= self.__speed

        elif self.__direction == "DOWN":
            self.__eyesUp = self.__eyesDown
            self.head.y += self.__speed

        elif self.__direction == "UP":
            self.__eyesUp = self.__eyesDown
            self.head.y -= self.__speed

    def followAlong(self):
        self.body.insert(0, self.head)
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        self.body.remove(self.head)
        self.moveSnake()

    def snakeAteApple(self, apple):
        if self.head.colliderect(apple.getApple()):
            return True

    def addBodyPartToSnake(self):
        self.body.append(pygame.Rect(self.lastBlock.x - 10, self.lastBlock.y, 30, 30))
        self.updateLastBlock()

    def updateLastBlock(self):
        self.lastBlock = self.body[len(self.body) - 1]

    def checkForCollision(self):
        # border collision
        if self.head.x > 1155:
            self.head.x = 1155
            return True
        elif self.head.x < 14:
            self.head.x = 14
            return True
        elif self.head.y > 570:
            self.head.y = 570
            return True
        elif self.head.y < 15:
            self.head.y = 15
            return True

        # body collision
        return self.head in self.body[1:]
