from assets import *
import pygame, random, copy
from Piece import Piece

pygame.init()
class Grid:
    
    def __init__(self):
        self.width = gridWidth
        self.height = gridHeight
        self.grid = EMPTYGRID

    def getColor(self, spot):
        color = WHITE
        if spot == 1:
            color = RED
        elif spot == 2:
            color = BLUE
        elif spot == 3:
            color = GREEN
        elif spot == 4:
            color = ORANGE
        elif spot == 5:
            color = YELLOW
        elif spot == 6:
            color = PURPLE
        elif spot == 7:
            color = LIGHTBLUE
        return color

    def drawGrid(self, screen, highlightCoords, piece, placePiece):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if (i, j) not in piece.coordSet or placePiece == False:
                    pygame.draw.rect(screen, self.getColor(self.grid[i][j]), (j * SQSIZE + 50, i * SQSIZE + 25, SQSIZE, SQSIZE))
                else:
                    pygame.draw.rect(screen, piece.color, (j * SQSIZE + 50, i * SQSIZE + 25, SQSIZE, SQSIZE))
        for i in range(len(self.grid) + 1):
            pygame.draw.line(screen, BLACK, (50, (i* SQSIZE) + 25), (gridWidth + 50, (i* SQSIZE) + 25), width=1)
        for i in range(len(self.grid[0]) + 1):
            pygame.draw.line(screen, BLACK, ((i * SQSIZE) + 50, 25), ((i * SQSIZE) + 50, gridHeight + 25), width=1)
        if placePiece:
            for coord in highlightCoords:
                s = pygame.Surface((SQSIZE, SQSIZE))
                s.set_alpha(100)
                s.fill(pygame.Color(piece.color))
                screen.blit(s, (coord[1]*SQSIZE + 50, coord[0]*SQSIZE + 25))

    def editGrid(self, coords, val):
        if coords[0] >= 0:
            self.grid[coords[0]][coords[1]] = val

    def checkGridChange(self, coordSet, takenCoords, placePiece):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] not in coordSet or placePiece == False:
                    self.grid[i][j] = 0
                
        for coord in takenCoords:
            self.grid[coord[0][0]][coord[0][1]] = coord[1]

        lines = 0
        newGrid = copy.deepcopy(self.grid)
        takenCoords.clear()
        for i in range(GRIDCOLS):
            if 0 not in newGrid[i]:
                lines += 1
                newGrid.pop(i)
                newGrid.insert(0, copy.deepcopy(EMPTYGRID[0]))
        
        self.grid = copy.deepcopy(newGrid)

        for i in range(GRIDCOLS):
            for j in range(GRIDROWS):
                if self.grid[i][j] != 0:
                    takenCoords.append(((i, j), self.grid[i][j]))


        return lines, takenCoords, self.grid

    def holdGraphic(self, piece, screen):
        piece.drawPiece(screen, 500, 100)

    def nextGraphic(self, currPieces, screen):
        space = SQSIZE * 2
        for i in range(3):
            if len(currPieces) <= 3:
                random.shuffle(pieces)
                for piece in pieces:
                    currPieces.append(piece)
                random.shuffle(currPieces)
            piece = Piece(currPieces[i])
            piece.createPiece()
            piece.drawPiece(screen, 520, 300 + i * space)

    def isGameOver(self, takenCoords):
        for coord in takenCoords:
            if coord[0][0] == 0:
                return True
        return False


# lines = 0
# takenCoords = []
# for i in range(len(self.grid)):
#     if 0 not in self.grid[i]:
#         lines += 1
#         for j in range(len(self.grid), 0, -1):
#             if j <= i and j > 0:
#                 for h in range(len(self.grid[0])):
#                     self.grid[j][h] = self.grid[j - 1][h]
#             elif j == 0:
#                 self.grid[j] = EMPTYGRID[0]

pygame.quit()