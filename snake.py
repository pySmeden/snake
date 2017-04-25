import pygame, sys, time, random, pygame.gfxdraw

from pygame.locals import *

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
WINDOWSIZE = (WINDOWWIDTH, WINDOWHEIGHT) # width and height of game window
FPS = 8 #

#            R    G    B
WHITE   = (255, 255, 255)
BLACK   = (  0,   0,   0)
RED     = (255,   0,   0)
GREEN   = ( 51, 153,  51)
GREY    = (194, 194, 194)

restartVal = None
highScore = 0

BGCOLOR = WHITE
clock = pygame.time.Clock()
snakeLength = 10 # no. of boxes the inital snake is built of
snakeSize   = 20 # size of each box the snake is built of
moveStep    = snakeSize # syntatic sugar

def main():
    
    global FPSCLOCK, DISPLAYSURF, FPS, restartVal, highScore
    
    replay = restart(restartVal)
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode(WINDOWSIZE)
    pygame.display.set_caption('Happy Snek!')
    DISPLAYSURF.fill(WHITE)
    
    xHead = int(WINDOWWIDTH/2) # x-position of the snakes head
    yHead = int(WINDOWHEIGHT/2) # x-position of the snakes head
    movex, movey = moveStep, 0
    score = 0
    snakePositionStart = snakeStartCoords(xHead, yHead)
    snakePositionOld = snakePositionStart
    xRand, yRand = generateSnakeFoodPosition(snakePositionOld)

    pygame.display.update()
    
    if replay is False:
        StartMenu()
    
    gameLoop = True
    
    while gameLoop is True: # main game loop
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                gameLoop = False
                pygame.mixer.music.stop()
                pygame.display.quit()
                pygame.quit
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_UP and movey != moveStep:
                    movey, movex = -moveStep, 0
                if event.key == pygame.K_DOWN and movey != -moveStep:
                     movey, movex = moveStep, 0
                if event.key == pygame.K_LEFT and movex != moveStep:
                     movex, movey = -moveStep, 0
                if event.key == pygame.K_RIGHT and movex != -moveStep:
                     movex, movey = moveStep, 0
                

        yHead += movey
        xHead += movex
        
        DISPLAYSURF.fill(WHITE)
        snakePositionNew = updateSnakeCoords(xHead, yHead, snakePositionOld)

        if selfCollision(snakePositionNew) is True or wallCollision(xHead, yHead) is True:
            crashSound()
            gameLostMenu(score,snakePositionNew)
            pygame.display.update()
            restartVal = True
            restart(restartVal)
            main()

        if wallCollision(xHead, yHead):
            crashSound()
            gameLostMenu(score,snakePositionNew)
            pygame.display.update()
            restartVal = True
            restart(restartVal)
            drawSnake(snakePositionNew)
            main()
        
        if xHead == xRand and yHead == yRand:
            eatSound()
            xRand, yRand = generateSnakeFoodPosition(snakePositionNew)
            snakePositionNew = growSnake(snakePositionNew, snakePositionOld)
            score += 10
        if score > highScore:
            highScore = score
            
        drawSnake(snakePositionNew)
        apple(xRand, yRand)
        
        scoreBoard(str(score))
        highScoreBoard(str(highScore))
        clock.tick(FPS)
        
        pygame.display.update()
        snakePositionOld = snakePositionNew
        

def drawGreenBox(x, y):
    
    pygame.draw.rect(DISPLAYSURF, WHITE, (x, y, snakeSize, snakeSize))
    pygame.draw.rect(DISPLAYSURF, GREEN, (x-1, y-1, snakeSize-1, snakeSize-1))
    

def apple(x, y):
    appleIMG = pygame.image.load('apple.png').convert()
    appleIMG = pygame.transform.scale(appleIMG, (snakeSize, snakeSize))
    DISPLAYSURF.blit(appleIMG, (x, y))


def restart(restartVal):
    if restartVal == None:
        return False
    else:
        return True
  
def drawSnake(snakeCoords):
    
    for i in range(len(snakeCoords)):
        x = snakeCoords[i][0]
        y = snakeCoords[i][1]
        drawGreenBox(x, y)

def snakeStartCoords(xHead, yHead):
    snake = []
    for i in range(snakeLength):
        if i == 0:
            snake.append([xHead, yHead])
        else:
            xHead -= snakeSize
            snake.append([xHead, yHead])
    return snake        


def generateSnakeFoodPosition(snakePositionOld):
    xRand = (int(random.uniform(0, WINDOWWIDTH)) / snakeSize) * snakeSize
    yRand = (int(random.uniform(0, WINDOWHEIGHT)) / snakeSize) * snakeSize
    Y = []
    X = []
    for xy in snakePositionOld:
        X.append(xy[0])
        Y.append(xy[1])

    while (xRand in X) and (yRand in Y): # continue looping if the generated food is on the snake
            xRand = (int(random.uniform(100, WINDOWWIDTH - 100)) / snakeSize) * snakeSize
            yRand = (int(random.uniform(150, WINDOWHEIGHT - 100)) / snakeSize) * snakeSize  

    return xRand, yRand

def selfCollision(snakePositionNew):
    count = 0
    for section in snakePositionNew:
        if snakePositionNew.count(section) > 1:
            count += 1
            
    if count > 1:
        return True
    elif count < 1:
        return False

def wallCollision(xHead, yHead):
    
    if xHead == -snakeSize or xHead == 640:
        return True
    elif yHead == -snakeSize or yHead == 480 + snakeSize:
        return True
    else:
        return False

def gameLostMenu(score, snakeCoords):
    
    sizeFont = lostMenuText()
    menuLoop = True
    mousex = 0
    mousey = 0
    #image = pygame.image.load('apple.png').convert()
    #image = pygame.transform.scale(image, (snakeSize, snakeSize))
    #image.set_alpha(128)
    #DISPLAYSURF.blit(image, (100, 100))
    #pygame.display.update()
    
    while menuLoop is True:
        
        mouseClicked = False
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.mixer.music.stop()
                gameLoop = False
                pygame.display.quit()
                pygame.quit
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
                if (mousex >= 200 and mousex <= sizeFont[0] + 200):
                    if (mousey >= 240 and mousey <= sizeFont[1] + 240):
                        pygame.mixer.music.stop()
                        pygame.display.quit()
                        pygame.quit
                        sys.exit()
                if (mousex >= 200 and mousex <= sizeFont[0] + 200):
                    if (mousey >= 190 and mousey <= sizeFont[1] + 190):
                        menuLoop = False


        scoreBoard(str(score))
        highScoreBoard(str(highScore))
    
        lostMenuText()

        pygame.display.update()

def StartMenu():
    
    DISPLAYSURF.fill(GREY)
    sizeFont = startMenuText()
    pygame.display.update()
    menuLoop = True
    mousex = 0
    mousey = 0
    pygame.mixer.init()

    pygame.mixer.music.load('menuMusic.mp3')

    pygame.mixer.music.play(-1)
    
    while menuLoop is True:
        
        mouseClicked = False
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                gameLoop = False
                pygame.mixer.music.stop()
                pygame.display.quit()
                pygame.quit
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
                if (mousex >= 200 and mousex <= sizeFont[0] + 200):
                    if (mousey >= 240 and mousey <= sizeFont[1] + 240):
                        pygame.mixer.music.stop()
                        pygame.display.quit()
                        pygame.quit
                        sys.exit()
                if (mousex >= 200 and mousex <= sizeFont[0] + 200):
                    if (mousey >= 190 and mousey <= sizeFont[1] + 190):
                        menuLoop = False
                
        DISPLAYSURF.fill(GREY)
        startMenuText()
        pygame.display.update()
    
def scoreBoard(score):
    fontObj = pygame.font.Font('BirdyGame.ttf', 25)
 
    scoreNum = fontObj.render(score, True, BLACK)
    scoreText = fontObj.render('SCORE: ', True, BLACK)
    
    DISPLAYSURF.blit(scoreText, (10, 10))
    DISPLAYSURF.blit(scoreNum, (150, 10))

def highScoreBoard(highScore):
    
    fontObj = pygame.font.Font('BirdyGame.ttf', 25)
 
    scoreNum = fontObj.render(highScore, True, BLACK)
    scoreText = fontObj.render('HIGHSCORE: ', True, BLACK)
    
    DISPLAYSURF.blit(scoreText, (350, 10))
    DISPLAYSURF.blit(scoreNum, (575, 10))

def lostMenuText():
    
    fontObj = pygame.font.Font('BirdyGame.ttf', 32)
    titleObj = pygame.font.Font('BirdyGame.ttf', 42)
    
    mainMenuTitleText = titleObj.render('You Crashed!', True, BLACK)
    startGameText = fontObj.render('Restart Game', True, BLACK)
    exitGameText = fontObj.render('Exit Game', True, BLACK)

    sizetitleObj = mainMenuTitleText.get_size()
    sizefontObj  = exitGameText.get_size()
    
    DISPLAYSURF.blit(mainMenuTitleText, (140, 140))
    DISPLAYSURF.blit(startGameText, (140, 190))
    DISPLAYSURF.blit(exitGameText, (140, 240))

    return sizefontObj

def startMenuText():
    
    fontObj = pygame.font.Font('BirdyGame.ttf', 32)
    titleObj = pygame.font.Font('BirdyGame.ttf', 42)
    
    mainMenuTitleText = titleObj.render('Main Menu', True, BLACK)
    startGameText = fontObj.render('Start Game', True, BLACK)
    exitGameText = fontObj.render('Exit Game', True, BLACK)

    sizetitleObj = mainMenuTitleText.get_size()
    sizefontObj  = exitGameText.get_size()
    
    DISPLAYSURF.blit(mainMenuTitleText, (180, 140))
    DISPLAYSURF.blit(startGameText, (180, 190))
    DISPLAYSURF.blit(exitGameText, (180, 240))

    return sizefontObj
    

def eatSound():
    soundObj = pygame.mixer.Sound('Powerup.wav')
    soundObj.play()

def crashSound():
    soundObj = pygame.mixer.Sound('Gameover2.wav')
    soundObj.play()

def growSnake(snakePositionNew, snakePositionOld):
    snakePositionNew.append(snakePositionOld[-1])
    return snakePositionNew


def updateSnakeCoords(xHead, yHead, snakeOldCoords):
    snake = []
    snake.append([xHead, yHead])
    del snakeOldCoords[-1]
    for xy in snakeOldCoords:
        snake.append(xy)
    return snake



    
if __name__ == '__main__':
    main()
