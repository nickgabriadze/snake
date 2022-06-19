import pygame
from Apple import Apple
from Snake import Snake
pygame.init()
pygame.mixer.init()


class SnakeGame:
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
        Frames = 24
        self.snake = Snake()
        self.apple = Apple()
        while self.running:
            self.clock.tick(Frames)
            self.update()
            self.render()
            self.events()

            self.displayScore()
            pygame.display.flip()
        self.cleanUp()

    def init(self):
        self.screen = pygame.display.set_mode((self.__displayWIDTH, self.__displayHEIGHT))
        pygame.display.set_caption("Snake")
        windowIcon = pygame.image.load("SnakeAssets/WindowIcon.png").convert(self.screen)
        pygame.display.set_icon(windowIcon)
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

    def displayScore(self):
        scoreFont = pygame.font.Font("SnakeAssets/BungeeShade-Regular.ttf", 40)
        scoreText = scoreFont.render(f"Score: {self.__gameScore}", False, (0, 80, 200))
        gameOverText = scoreFont.render("Game Over!", False, (200, 0, 20))
        x, y = 100, 625
        if self.__inGame == 2:
            self.screen.blit(scoreText, (x, y))
            self.displayBestScore()
        if self.__gameOver:
            self.screen.blit(gameOverText, (self.__displayWIDTH // 2 - 150, self.__displayHEIGHT - 80))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        if self.__inGame == 2:
            self.screen.fill(0)
            self.gameScoreMsg()
            self.screen.blit(self.__gameScreen, (0, 0))
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
            font = pygame.font.Font("SnakeAssets/BungeeShade-Regular.ttf", 40)
            gameOverText = font.render(f"Score: {self.__gameScore}", False, (173, 47, 49))

            toRead = open("SnakeAssets/bestScore.txt", "r")

            actualBestScore = int(toRead.readlines()[0])

            if self.__gameScore > actualBestScore:
                toWrite = open("SnakeAssets/bestScore.txt", "w")
                toWrite.write(str(self.__gameScore))
                actualBestScore = self.__gameScore
                toWrite.close()

            toRead.close()
            bestScoreFont = pygame.font.Font("SnakeAssets/BungeeShade-Regular.ttf", 40)
            bestScoreText = bestScoreFont.render(f"Best Score: {actualBestScore}", False, (173, 47, 50))
            askForRestartOrQuitFont = pygame.font.Font("SnakeAssets/BungeeShade-Regular.ttf", 40)
            askForRestartOrQuit = askForRestartOrQuitFont.render("Press 'R' to Restart or 'Q' to Quit", False,
                                                                 (173, 47, 55))

            self.screen.blit(gameOverText, (self.__displayWIDTH // 2 - 120, self.__displayHEIGHT // 2 - 150))
            self.screen.blit(bestScoreText, (self.__displayWIDTH // 2 - 200, self.__displayHEIGHT // 2 - 100))
            self.screen.blit(askForRestartOrQuit, (self.__displayWIDTH // 2 - 450, self.__displayHEIGHT // 2 - 50))
            self.checkForRestart()
            pygame.display.flip()

    def cleanUp(self):
        self.screen.fill(10)

    def displayBestScore(self):
        toRead = open("SnakeAssets/bestScore.txt", "r")

        actualBestScore = int(toRead.readlines()[0])

        if self.__gameScore > actualBestScore:
            toWrite = open("SnakeAssets/bestScore.txt", "w")
            toWrite.write(str(self.__gameScore))
            actualBestScore = self.__gameScore
            toWrite.close()

        toRead.close()
        bestScoreFont = pygame.font.Font("SnakeAssets/BungeeShade-Regular.ttf", 40)
        bestScoreText = bestScoreFont.render(f"Best: {actualBestScore}", False, (0, 80, 200))
        self.screen.blit(bestScoreText, (880, 625))

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
