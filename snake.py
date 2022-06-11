import pygame
from random import randint as randomPos

pygame.init()
pygame.mixer.init()


class Snake(object):
    __mainPositionX = 300
    __mainPositionY = 300
    __direction = "RIGHT"

    def __init__(self):
        self.head = pygame.Rect(self.__mainPositionX, self.__mainPositionY, 30, 30)
        self.body = [pygame.Rect(self.__mainPositionX - 15, self.__mainPositionY, 30, 30),
                     pygame.Rect(self.__mainPositionX - 30, self.__mainPositionY, 30, 30),
                     pygame.Rect(self.__mainPositionX - 45, self.__mainPositionY, 30, 30),
                     pygame.Rect(self.__mainPositionX - 60, self.__mainPositionY, 30, 30)]
        self.lastBlock = self.body[len(self.body) - 1]

    def displaySnake(self, surface):
        pygame.draw.rect(surface, (10, 240, 10), self.head,  border_radius=7)
        for bodyPart in self.body:
            pygame.draw.rect(surface, (10, 240, 10), bodyPart, border_radius=7)

    def collideInItself(self):
        for bodyPart in self.body:
            if self.head.x == bodyPart.x:
                pass

    def moveSnake(self):
        pressedKeys = pygame.key.get_pressed()

        if pressedKeys[pygame.K_LEFT] or pressedKeys[pygame.K_a] and self.__direction != "RIGHT":
            self.__direction = "LEFT"
        elif pressedKeys[pygame.K_RIGHT] or pressedKeys[pygame.K_d] and self.__direction != "LEFT":
            self.__direction = "RIGHT"
        elif pressedKeys[pygame.K_DOWN] or pressedKeys[pygame.K_s] and self.__direction != "UP":
            self.__direction = "DOWN"
        elif pressedKeys[pygame.K_UP] or pressedKeys[pygame.K_w] and self.__direction != "DOWN":
            self.__direction = "UP"

        if self.__direction == "RIGHT":
            self.head.x += 10

        elif self.__direction == "LEFT":
            self.head.x -= 10

        elif self.__direction == "DOWN":
            self.head.y += 10

        elif self.__direction == "UP":
            self.head.y -= 10

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


class App:
    __welcomeScreen = pygame.image.load("SnakeAssets/SnakeWelcomeScreen.png")
    __gameScreen = pygame.image.load("SnakeAssets/SnakeBG.png")
    __inGame = 0
    __gameScore = 0
    __gameOver = False
    __displayWIDTH = 1200
    __displayHEIGHT = 700

    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None
        self.snake = None
        self.apple = None

    def run(self):
        self.init()
        FPS = 24
        self.snake = Snake()
        self.apple = Apple()
        while self.running:
            self.clock.tick(FPS)
            self.update()
            self.render()
            self.events()
            pygame.display.flip()
        self.cleanUp()

    def init(self):
        self.screen = pygame.display.set_mode((self.__displayWIDTH, self.__displayHEIGHT))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        self.running = True
        if self.__inGame == 0:
            self.screen.blit(self.__welcomeScreen, (0, 0))
            self.__inGame += 1

    def update(self):
        self.events()
        pressedKeys = pygame.key.get_pressed()
        if self.__inGame == 1:
            if pressedKeys[pygame.K_p]:
                self.cleanUp()
                self.screen.blit(self.__gameScreen, (0, 0))
                self.__inGame += 1  # 2

    def gameScoreMsg(self):
        if self.__gameScore >= 10:
            pygame.display.set_caption("Wow, you've got some skills!")
        elif self.__gameScore >= 50:
            pygame.display.set_caption("Who are you?!")
        elif self.__gameScore >= 100:
            pygame.display.set_caption("I have no words for that score, Keep going!")
        elif self.__gameScore == 0:
            pygame.display.set_caption("Have fun!")

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        if self.__inGame == 2:
            self.screen.fill(0)
            self.gameScoreMsg()
            self.screen.blit(self.__gameScreen, (0, 0))
            scoreFont = pygame.font.Font("SnakeAssets/KdamThmorPro-Regular.ttf", 40)
            scoreText = scoreFont.render(f"Score: {self.__gameScore}", False, (255, 255, 255))
            self.screen.blit(scoreText, (30, 620))
            self.snake.displaySnake(self.screen)
            self.apple.displayApple(self.screen)

            self.snake.followAlong()
            if self.snake.checkForCollision():
                self.__gameOver = True
                pygame.mixer.music.load("SnakeAssets/GameOver.ogg")
                pygame.mixer.music.play()
                self.__inGame += 1  # 3

            if self.snake.snakeAteApple(self.apple):
                pygame.mixer.music.load("SnakeAssets/AppleEatingSound.ogg")
                pygame.mixer.music.play()
                self.apple.changeApplePosition()
                self.__gameScore += 1
                self.snake.addBodyPartToSnake()

    def render(self):
        if self.__gameOver is True:
            pygame.display.set_caption("Game Over!")
            font = pygame.font.Font("SnakeAssets/KdamThmorPro-Regular.ttf", 40)
            gameOverText = font.render(f"Score: {self.__gameScore}", False, (173, 47, 49))

            toRead = open("SnakeAssets/bestScore.txt", "r")

            actualBestScore = int(toRead.readlines()[0])

            if self.__gameScore > actualBestScore:
                toWrite = open("SnakeAssets/bestScore.txt", "w")
                toWrite.write(str(self.__gameScore))
                actualBestScore = self.__gameScore
                toWrite.close()

            toRead.close()
            bestScoreFont = pygame.font.Font("SnakeAssets/KdamThmorPro-Regular.ttf", 40)
            bestScoreText = bestScoreFont.render(f"Best Score: {actualBestScore}", False, (173, 47, 50))
            askForRestartOrQuitFont = pygame.font.Font("SnakeAssets/KdamThmorPro-Regular.ttf", 50)
            askForRestartOrQuit = askForRestartOrQuitFont.render("Press 'R' to Restart or 'Q' to Quit", False,
                                                                 (173, 47, 55))

            self.screen.blit(gameOverText, (self.__displayWIDTH // 2 - 60, self.__displayHEIGHT // 2 - 150))
            self.screen.blit(bestScoreText, (self.__displayWIDTH // 2 - 100, self.__displayHEIGHT // 2 - 100))
            self.screen.blit(askForRestartOrQuit, (self.__displayWIDTH // 2 - 330, self.__displayHEIGHT // 2 - 50))
            self.checkForRestart()
            pygame.display.flip()

    def cleanUp(self):
        self.screen.fill(0)

    def checkForRestart(self):
        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[pygame.K_r]:
            newApp = App()
            newApp.run()
        if pressedKeys[pygame.K_q]:
            self.running = False


if __name__ == "__main__":
    app = App()
    app.run()