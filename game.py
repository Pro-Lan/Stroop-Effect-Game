import highScoreModule
import pygame
import random

# Initialize game surface
pygame.init()
screen = pygame.display.set_mode((600, 600))
background = pygame.Surface(screen.get_size())
pygame.display.set_caption("Stroop Effect Game")


class button:
    """Class used for the two menu buttons"""

    def __init__(self, screen, left, top, width, height, name):
        self.label = name
        self.buttonColor = (255, 0, 0)
        self.buttonRect = pygame.Rect(left, top, width, height)
        self.buttonSurface = pygame.Surface(self.buttonRect.size)

    def drawButton(self, screen):
        """Class used for the two menu buttons"""
        self.buttonSurface.fill(self.buttonColor)
        self.buttonSurface.convert()
        screen.blit(self.buttonSurface, (self.buttonRect.x, self.buttonRect.y))
        pygame.draw.rect(self.buttonSurface, self.buttonColor, self.buttonRect, 1)
        self.drawText(screen)

    def drawText(self, screen):
        """Writes the buttons name on the button surface"""
        buttonTextFont = pygame.font.SysFont("ariel", 50)
        buttonText = buttonTextFont.render(self.label, True, (0, 55, 90), self.buttonColor)
        buttonText = buttonText.convert()
        screen.blit(buttonText, self.buttonRect)


class colorWord:
    """class used for the coloured words that get displayed on the
    screen during the gameplay"""

    def __init__(self, fontColor, word):
        wordFont = pygame.font.SysFont("ariel", 72)
        self.theColorText = wordFont.render(word, True, fontColor)
        self.position = [random.randrange(40, 420), random.randrange(40, 440)]

    def drawWord(self, screen):
        screen.blit(self.theColorText, self.position)

    def moveWord(self, screen, vector, backgroundColor):
        wordClearSurface = pygame.Surface(self.theColorText.get_size())
        wordClearSurface.fill(backgroundColor)
        screen.blit(wordClearSurface, self.position)

        if not (0 < self.position[0] < 420):
            vector[0] = -1 * vector[0]
        if not (40 < self.position[1] < 440):
            vector[1] = -1 * vector[1]

        self.position[0] += vector[0]
        self.position[1] += vector[1]
        screen.blit(self.theColorText, self.position)


def drawMenu(screen, background, playButton, highScoreButton):
    """draws the background and main menu buttons to the screen"""
    background.fill((153, 255, 153))
    background = background.convert()
    screen.blit(background, (0, 0))
    playButton.drawButton(screen)
    highScoreButton.drawButton(screen)

    titleFont = pygame.font.SysFont("impact", 60)
    titleText = titleFont.render("Stroop Effect game", True, (75, 0, 130))
    titleText.convert()
    screen.blit(titleText, (60, 50))

    instructionFont = pygame.font.SysFont("verdana", 32)
    instructionText = instructionFont.render("Click the Color of the word!",
                                             True, (220, 20, 60))
    instructionText.convert()
    screen.blit(instructionText, (100, 450))
    pygame.display.update()


def playGame():
    """the main gameplay loop, draws colours to the screen in different
        font colours and detects when the player clicks the correct button,
        then increments their score by one"""
    gameBackground = pygame.Surface((600, 500))
    gameBackground.fill((255, 255, 255))
    gameBackground.convert()

    # the colours six colours that will be used and their corresponding RGB values
    colors = (("Red", (255, 0, 0)), ("Green", (0, 255, 0)), ("Blue", (0, 0, 255)),
              ("Yellow", (255, 255, 0)), ("Pink", (255, 20, 147)), ("Purple", (128, 0, 128)))

    colorButtonRects = []
    drawGameButtons(colorButtonRects, colors)
    userScore = 0
    timer = 0.0  # stores the time that the user has been playing
    timelimit = 60 # time limit the user has to score as many as possible
    FPS = 60

    while timer < timelimit:
        clock = pygame.time.Clock()
        milliseconds = clock.tick(FPS)
        timer += milliseconds / 1000
        isMoving = False

        fontColorIndex = random.randrange(0, 6)
        fontColor = colors[fontColorIndex][1]
        word = colors[random.randrange(0, 6)][0]

        theColorWord = colorWord(fontColor, word)

        if userScore >= 10:
            backGroundColorIndex = random.randrange(0, 6)

            while backGroundColorIndex == fontColorIndex:
                backGroundColorIndex = random.randrange(0, 6)
            backgroundColor = colors[backGroundColorIndex][1]
            gameBackground.fill(backgroundColor)
        if userScore >= 20:
            isMoving = True
            movementVector = [random.randrange(-5, 5), random.randrange(-5, 5)]

        screen.blit(gameBackground, (0, 0))

        displayHeaderInfo("Score: " + str(userScore), 1, (255, 255, 0))

        theColorWord.drawWord(screen)
        pygame.display.update()

        userClicked = False
        while userClicked == False and timer < timelimit:
            if isMoving:
                theColorWord.moveWord(screen, movementVector, backgroundColor)

            milliseconds = clock.tick(FPS)
            timer += milliseconds / 1000

            displayHeaderInfo("Timer: " + str(round(timer)), 2, (255, 0, 0))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(colorButtonRects)):
                        # when mouse button is pressed, the cursor position is
                        # checked to see if it's over the correct button
                        if (colorButtonRects[i].collidepoint(pygame.mouse.get_pos())
                                and i == fontColorIndex):
                            userClicked = True
                            userScore += 1
                            screen.blit(gameBackground, (0, 0))
    gameBackground.fill((255, 255, 255))
    screen.blit(gameBackground, (0, 0))
    highScoreModule.updateHighScores(userScore, screen)


def drawGameButtons(buttonRects, colors):
    """draws the game buttons to the bottom of the screen and creates rects
        around them, and displays colour (in words) on the button"""
    buttonColor = (250, 235, 215)
    buttons = list()

    for i in range(len(colors)):
        if i <= 2:
            # puts the first three buttons on the top row
            buttonRects.append(pygame.Rect(i * 200, 500, 200, 50))
        else:
            # puts the second three buttons on the bottom row
            buttonRects.append(pygame.Rect((i - 3) * 200, 550, 200, 50))

        buttons.append(pygame.Surface(buttonRects[i].size))

        buttons[i].fill(buttonColor)
        buttons[i].convert()

        screen.blit(buttons[i], (buttonRects[i].x, buttonRects[i].y))
        pygame.draw.rect(buttons[i], buttonColor, buttonRects[i], 30)

        buttonFont = pygame.font.SysFont("ariel", 50)

        buttonText = buttonFont.render(colors[i][0], True, (0, 55, 90, 0))
        buttonText = buttonText.convert_alpha()
        screen.blit(buttonText, (buttonRects[i].x + 50, buttonRects[i].y + 5))


def displayHeaderInfo(text, position, color):
    Font = pygame.font.SysFont("ariel", 50)
    Text = Font.render(text, True, (0, 0, 0), (255, 255, 255))
    Text = Text.convert()
    screen.blit(Text, (600 - (200 * position), 0))


playButton = button(screen, 200, 200, 200, 50, "       Play")
highScoreButton = button(screen, 200, 300, 200, 50, " High Score")

drawMenu(screen, background, playButton, highScoreButton)

menuloop = True
while menuloop:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            menuloop = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if playButton.buttonRect.collidepoint(pygame.mouse.get_pos()):
                playGame()
                drawMenu(screen, background, playButton, highScoreButton)
            elif highScoreButton.buttonRect.collidepoint(pygame.mouse.get_pos()):
                highScoreModule.displayHighScores(screen, background)
                drawMenu(screen, background, playButton, highScoreButton)

        elif playButton.buttonRect.collidepoint(pygame.mouse.get_pos()):

            if event.type == pygame.MOUSEBUTTONDOWN:
                playButton.buttonColor = (255, 255, 0)
            else:
                playButton.buttonColor = (255, 165, 0)
            playButton.drawButton(screen)
            pygame.display.update()

        elif highScoreButton.buttonRect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN:
                highScoreButton.buttonColor = (255, 255, 0)
            else:
                highScoreButton.buttonColor = (255, 165, 0)
            highScoreButton.drawButton(screen)
            pygame.display.update()
        else:
            playButton.buttonColor = (255, 0, 0)
            playButton.drawButton(screen)
            highScoreButton.buttonColor = (255, 0, 0)
            highScoreButton.drawButton(screen)
            pygame.display.update()
pygame.quit()
