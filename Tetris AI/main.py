import pygame, random, time, copy
from assets import *
from grid import Grid
from Piece import Piece
from agent import Agent
from gameControl import *

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
pygame.display.set_caption("Tetris!")

grid = Grid()
agent = Agent()
hold = False
currPieces = pieces.copy()
random.shuffle(currPieces)
'''
Generates value for current piece and hold piece then picks the one with the highest value
'''
pickedPiece = currPieces[0]
piece = Piece(pickedPiece)
currPieces.pop(currPieces.index(pickedPiece))
piece.createPiece()
agent.generateAllMoves([], copy.deepcopy(piece))
AImove, AImoveScore = agent.evaluateMove()
tryPiece = Piece(currPieces[0])
tryPiece.createPiece()
agent.generateAllMoves([], copy.deepcopy(tryPiece))
holdMove, holdMoveScore = agent.evaluateMove()
if holdMoveScore > AImoveScore:
    AImove = holdMove
    holdPiece = piece
    piece = tryPiece
    currPieces.pop(0)
    hold = True
else:
    holdPiece = None

'''
Creates timer that moves down piece
'''
speed = 500
PIECEDOWN = pygame.USEREVENT
pygame.time.set_timer(PIECEDOWN, speed)
PIECEMOVE = pygame.USEREVENT + 1
pygame.time.set_timer(PIECEMOVE, 1000)

takenCoords = []

movement = [False, False, False] # [Right, Left, Down]

score = 0
speedup = True
placePiece = True

'''
Draws attributes to the screen like the hold and next piece
'''
def drawGraphics():
    screen.fill(WHITE)
    highlightCoords = piece.highlightPiece(takenCoords)
    grid.drawGrid(screen, highlightCoords, piece, placePiece)
    drawText(screen, "Hold:", 20, (570, 40))
    if hold:
        grid.holdGraphic(holdPiece, screen)
    drawText(screen, "Next:", 20, (570, 250))
    grid.nextGraphic(currPieces, screen )
    drawText(screen, f"Lines Cleared: {score}", 20, (780, 10))

run = True
while run:
    clock.tick(FPS)
    '''
    Moves the piece down if the timer is triggered
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == PIECEDOWN and movement[2] == False:
            piece.moveDownPiece()
            for move in movement:
                move = False
    '''
    Compares the current position of the piece to the AI move and if they are not the same move them, if they are the same slam down the piece
    '''
    if placePiece:
        if piece.phase - 1 != AImove[1]:
            piece.rotatePiece(takenCoords)
        elif piece.coordSet[0][1] != AImove[0]:
            if piece.coordSet[0][1] > AImove[0]:
                piece.movePieceLeft()
            elif piece.coordSet[0][1] < AImove[0]:
                piece.movePieceRight()
        else:
            piece.slam(takenCoords)
            for coord in piece.coordSet:
                takenCoords.append((coord, piece.type))
            agent.moves = []
            placePiece = False
    
    lines, takenCoords, grid.grid = grid.checkGridChange(piece.coordSet, takenCoords, placePiece)
    score += lines
    drawGraphics()
    '''
    If the piece is at the bottom reset all values related to the piece and generate a new one
    '''
    if piece.isBottom(takenCoords):
        if len(currPieces) == 3:
            random.shuffle(pieces)
            for piece in pieces:
                currPieces.append(piece)
            random.shuffle(currPieces)
        pickedPiece = currPieces[0]
        piece = Piece(pickedPiece)
        currPieces.pop(currPieces.index(pickedPiece))
        piece.createPiece()
        agent.generateAllMoves(copy.deepcopy(takenCoords), copy.deepcopy(piece))
        AImove, AImoveScore = agent.evaluateMove()
        if holdPiece == None:
            tryPiece = Piece(currPieces[0])
            tryPiece.createPiece()
            agent.generateAllMoves(copy.deepcopy(takenCoords), copy.deepcopy(tryPiece))
        else:
            agent.generateAllMoves(copy.deepcopy(takenCoords), copy.deepcopy(holdPiece))
        holdMove, holdMoveScore = agent.evaluateMove()
        if holdMoveScore > AImoveScore:
            if holdPiece == None:
                holdPiece = piece
                piece = Piece(currPieces.pop(0))
                piece.createPiece()
            else:
                Temp = piece
                piece = holdPiece
                holdPiece = Temp
            AImove = holdMove
            hold = True
        placePiece = True
    '''
    if the game is over print message and terminate the program
    '''
    if grid.isGameOver(takenCoords):
        print("Game Over")
        drawText(screen, "Game Over", 38, (WIDTH // 2 - 50, HEIGHT // 2 - 25))
        run = False
        print(score)
    pygame.display.flip()

time.sleep(5)