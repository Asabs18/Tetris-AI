import pygame, random
from assets import *
from grid import Grid
import copy

pygame.init()

class Agent:

    def __init__(self):
        self.moves = []

    def generateAllMoves(self, takenCoords, piece):
        ogPiece = copy.deepcopy(piece)
        for i in range(GRIDROWS):
            for j in range(4):
                currTakenCoords = copy.deepcopy(takenCoords)
                grid = Grid()
                grid.checkGridChange(piece.coordSet, currTakenCoords, True)
                for h in range(j):
                    piece.rotatePiece(currTakenCoords)
                hold = 0
                while piece.coordSet[0][1] != i:
                    if piece.coordSet[0][1] > i:
                        piece.movePieceLeft()
                    elif piece.coordSet[0][1] < i:
                        piece.movePieceRight()
                        if piece.coordSet[0][1] == hold:
                            break
                        else:
                            hold = piece.coordSet[0][1]
                piece.slam(currTakenCoords)
                for coord in piece.coordSet:
                    currTakenCoords.append((coord, piece.type))
                lines, currTakenCoords, grid.grid = grid.checkGridChange(piece.coordSet, currTakenCoords, False)
                self.moves.append((piece.coordSet[0][1], j, copy.deepcopy(grid), lines, currTakenCoords))
                piece = copy.deepcopy(ogPiece)

    def evaluateMove(self):
        bestMoveScore = 0
        bestMove = None
        currScore = 0
        HEIGHT = -2.38
        HOLE = -3.78
        BLOCKADE = -0.59
        CLEAR = 2.6
        TOUCHBLOCK = 3.97
        TOUCHWALL = 6.52
        TOUCHFLOOR = 0.65

        for move in self.moves:
            for i in range(GRIDCOLS):
                for j in range(GRIDROWS):
                    if move[2].grid[i][j] == 0 and move[2].grid[i - 1][j] != 0:
                        currScore += HOLE
                    if move[2].grid[i][j] == 0 and move[2].grid[i - 1][j] == 0 and move[2].grid[i-1][j] != 0:
                        currScore += HOLE * 2
                    if move[2].grid[i][j] != 0:
                        currScore += (GRIDCOLS - i) * HEIGHT
                    if move[2].grid[i][j] != 0:
                        if move[2].grid[i - 1][j] != 0:
                            currScore += TOUCHBLOCK
                        if i < GRIDCOLS - 1 :
                            if move[2].grid[i + 1][j] != 0:
                                currScore += TOUCHBLOCK
                        if j < GRIDROWS - 1:
                            if move[2].grid[i][j + 1] != 0: 
                                currScore += TOUCHBLOCK
                        if j > 1: 
                            if move[2].grid[i][j - 1] != 0:
                                currScore += TOUCHBLOCK
                    if i == GRIDCOLS - 1 and move[2].grid[i][j] != 0:
                        currScore += TOUCHFLOOR
                    if i == GRIDROWS - 1 or i == 0 and move[2].grid[i][j] != 0:
                        currScore += TOUCHWALL
                    if move[2].grid[i][j] != 0:
                        for h in range(i, 0, -1):
                            if move[2].grid[h][j] != 0 and move[2].grid[h - 1][j] == 0:
                                currScore += BLOCKADE
                    
                    currScore += move[3] * CLEAR
            if currScore > bestMoveScore or bestMove == None:
                bestMove = move
                bestMoveScore = currScore
            currScore = 0
        return bestMove, bestMoveScore


pygame.quit()