# Checkers
# By Syndney and Isabelle

# Based on Flippy
# http://inventwithpython.com/pygame
# Based on the "reversi.py" code that originally appeared in "Invent
# Your Own Computer Games with Python", chapter 15:
#   http://inventwithpython.com/chapter15.html

import random, sys, pygame, time, copy
from pygame.locals import *

FPS = 10 # frames per second to update the screen
WINDOWWIDTH = 640 # width of the program's window, in pixels
WINDOWHEIGHT = 480 # height in pixels
SPACESIZE = 50 # width & height of each space on the board, in pixels
BOARDWIDTH = 8 # how many columns of spaces on the game board
BOARDHEIGHT = 8 # how many rows of spaces on the game board
WHITE_CIRCLE = 'WHITE_CIRCLE' # an arbitrary but unique value
BLACK_CIRCLE= 'BLACK_CIRCLE' # an arbitrary but unique value
EMPTY_SPACE = 'EMPTY_SPACE' # an arbitrary but unique value

# Amount of space on the left & right side (XMARGIN) or above and below
# (YMARGIN) the game board, in pixels.
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * SPACESIZE)) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * SPACESIZE)) / 2)

#              R    G    B
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
GREEN      = (  0, 155,   0)
BRIGHTBLUE = (  0,  50, 255)
BROWN      = (174,  94,   0)
RED        = (203,  32,  39)
TAN        = (222, 188, 153)
TEXTBGCOLOR1 = BRIGHTBLUE
TEXTBGCOLOR2 = GREEN
GRIDLINECOLOR = BLACK
TEXTCOLOR = WHITE


def main():
    global MAINCLOCK, DISPLAYSURF, FONT, BIGFONT, BGIMAGE

    pygame.init()
    MAINCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Checkers')
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 32)

    # Set up the background image.
    boardImage = pygame.image.load('flippyboard.png')
    # Use smoothscale() to stretch the board image to fit the entire board:
    boardImage = pygame.transform.smoothscale(boardImage, (BOARDWIDTH * SPACESIZE, BOARDHEIGHT * SPACESIZE))
    boardImageRect = boardImage.get_rect()
    boardImageRect.topleft = (XMARGIN, YMARGIN)
    BGIMAGE = pygame.image.load('flippybackground.png')
    # Use smoothscale() to stretch the background image to fit the entire window:
    BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
    BGIMAGE.blit(boardImage, boardImageRect)

    # Run the main game.
    while True:
        if runGame() == False:
            break


def runGame():
    # Plays a single game of checkers each time this function is called.

    # Reset the board and game.
    mainBoard = getNewBoard()

    resetBoard(mainBoard)
    movepiece = None
    #turn = random.choice(['computer', 'player'])

    # Draw the starting board and ask the player what color they want.
    drawBoard(mainBoard,movepiece)
    playerTile, computerTile = [WHITE_CIRCLE,BLACK_CIRCLE]

    # Make the Surface and Rect objects for the "New Game"
    newGameSurf = FONT.render('New Game', True, TEXTCOLOR, TEXTBGCOLOR2)
    newGameRect = newGameSurf.get_rect()
    newGameRect.topright = (WINDOWWIDTH - 8, 10)

    while True: # main game loop
        # Draw the game board.
        drawBoard(mainBoard,movepiece)
        # Draw the "New Game" and "Hints" buttons.
        DISPLAYSURF.blit(newGameSurf, newGameRect)
        MAINCLOCK.tick(FPS)
        pygame.display.update()

        movexy = None
        while movexy == None:
            # Keep looping until the player clicks on a valid space.
            checkForQuit()
            for event in pygame.event.get(): # event handling loop
                if event.type == MOUSEBUTTONUP:
                    # Handle mouse click events
                    mousex, mousey = event.pos
                    if newGameRect.collidepoint( (mousex, mousey) ):
                        # Start a new game
                        return True
                    # movexy is set to a two-item tuple XY coordinate, or None value
                    movexy = getSpaceClicked(mousex, mousey)
                    if movexy != None and not isValidMove(mainBoard, playerTile, movexy[0], movexy[1]):
                        movexy = None
                    if movexy != None and mainBoard[movexy[0]][movexy[1]] != EMPTY_SPACE:
                        movepiece = movexy
                        
def translateBoardToPixelCoord(x, y):
    return XMARGIN + x * SPACESIZE + int(SPACESIZE / 2), YMARGIN + y * SPACESIZE + int(SPACESIZE / 2)

def drawBoard(board,movepiece):
    # Draw background of board.
    DISPLAYSURF.blit(BGIMAGE, BGIMAGE.get_rect())        
    isWhite = True
            
    # Draw the black & white tiles
    for x in range(BOARDWIDTH):
        isWhite = not isWhite
        for y in range(BOARDHEIGHT): 
            centerx, centery = translateBoardToPixelCoord(x, y)
            if isWhite:
                color = WHITE   
            else:
                color = BLACK
            isWhite = not isWhite 
            pygame.draw.rect(DISPLAYSURF, color, (centerx - 25, centery - 25, 50, 50))
            
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            centerx, centery = translateBoardToPixelCoord(x, y)
            if board[x][y] == WHITE_CIRCLE or board[x][y] ==BLACK_CIRCLE:
                if board[x][y] == WHITE_CIRCLE:
                    tileColor = RED
                else:
                    tileColor = TAN
                pygame.draw.circle(DISPLAYSURF, tileColor, (centerx, centery), int(SPACESIZE / 2) - 4)
                if movepiece != None and movepiece [0] == x and movepiece [1] == y:
                    pygame.draw.rect(DISPLAYSURF, RED, (centerx - 4, centery - 4, 8, 8))

def getSpaceClicked(mousex, mousey):
    # Return a tuple of two integers of the board space coordinates where
    # the mouse was clicked. (Or returns None not in any space.)
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if mousex > x * SPACESIZE + XMARGIN and \
               mousex < (x + 1) * SPACESIZE + XMARGIN and \
               mousey > y * SPACESIZE + YMARGIN and \
               mousey < (y + 1) * SPACESIZE + YMARGIN:
                return (x, y)
    return None

def resetBoard(board):
    # Blanks out the board it is passed, and sets up starting tiles.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            board[x][y] = EMPTY_SPACE

    # Add starting pieces to the center
    board[0][0] = WHITE_CIRCLE
    board[0][2] = WHITE_CIRCLE
    board[0][4] = WHITE_CIRCLE
    board[0][6] = WHITE_CIRCLE
    board[1][1] = WHITE_CIRCLE
    board[1][3] = WHITE_CIRCLE
    board[1][5] = WHITE_CIRCLE
    board[1][7] = WHITE_CIRCLE
    board[2][0] = WHITE_CIRCLE
    board[2][2] = WHITE_CIRCLE
    board[2][4] = WHITE_CIRCLE
    board[2][6] = WHITE_CIRCLE
    
    board[5][1] = BLACK_CIRCLE
    board[5][3] = BLACK_CIRCLE
    board[5][5] = BLACK_CIRCLE
    board[5][7] = BLACK_CIRCLE
    board[6][0] = BLACK_CIRCLE
    board[6][2] = BLACK_CIRCLE
    board[6][4] = BLACK_CIRCLE
    board[6][6] = BLACK_CIRCLE
    board[7][1] = BLACK_CIRCLE
    board[7][3] = BLACK_CIRCLE
    board[7][5] = BLACK_CIRCLE
    board[7][7] = BLACK_CIRCLE


def getNewBoard():
    # Creates a brand new, empty board data structure.
    board = []
    for i in range(BOARDWIDTH):
        board.append([EMPTY_SPACE] * BOARDHEIGHT)

    return board


def isValidMove(board, tile, xstart, ystart):
    return True # TODO: fix to do valid checkers move
    if board[xstart][ystart] != EMPTY_SPACE or not isOnBoard(xstart, ystart):
        return False


def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x < BOARDWIDTH and y >= 0 and y < BOARDHEIGHT


def checkForQuit():
    for event in pygame.event.get((QUIT, KEYUP)): # event handling loop
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    main()
