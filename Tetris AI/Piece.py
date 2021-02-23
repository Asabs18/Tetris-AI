from assets import *
import pygame

pygame.init()

class Piece:

    def __init__(self, type):
        self.type = type
        self.color = self.getColor(type)
        self.coordSet = []
        self.phase = 1
        self.pieceFunctions = {1: self.createLeftTwist, 2:self.createLeftL, 3:self.createRightTwist, 4: self.createRightL, 5: self.createBox, 6: self.createT, 7:self.createLine}
        self.rotateFunctions = {1: self.rotateLeftTwist, 2:self.rotateLeftL, 3: self.rotateRightTwist, 4: self.rotateRightL, 5: self.rotateBox, 6: self.rotateT, 7: self.rotateLine}

    def getColor(self, type):
        color = WHITE
        if type == 1:
            color = RED
        elif type == 2:
            color = BLUE
        elif type == 3:
            color = GREEN
        elif type == 4:
            color = ORANGE
        elif type == 5:
            color = YELLOW
        elif type == 6:
            color = PURPLE
        elif type == 7:
            color = LIGHTBLUE
        return color

    def createLine(self, TLCoord):
        self.coordSet.append(TLCoord)
        for i in range(3):
            self.coordSet.append((TLCoord[0], i + 1 + TLCoord[1]))

    def createLeftL(self, TLCoord):
        self.coordSet.append(TLCoord)
        self.coordSet.append((TLCoord[0] + 1, TLCoord[1]))
        self.coordSet.append((TLCoord[0] + 1, TLCoord[1] + 1))
        self.coordSet.append((TLCoord[0] + 1, TLCoord[1] + 2))

    def createRightL(self, TLCoord):
        self.coordSet.append(TLCoord)
        self.coordSet.append((TLCoord[0], TLCoord[1] + 1))
        self.coordSet.append((TLCoord[0], TLCoord[1] + 2))
        self.coordSet.append((TLCoord[0] - 1, TLCoord[1] + 2))

    def createBox(self, TLCoord):
        self.coordSet.append(TLCoord)
        self.coordSet.append((TLCoord[0] + 1, TLCoord[1]))
        self.coordSet.append((TLCoord[0], TLCoord[1] + 1))
        self.coordSet.append((TLCoord[0] + 1, TLCoord[1] + 1))

    def createRightTwist(self, TLCoord):
        self.coordSet.append(TLCoord)
        self.coordSet.append((TLCoord[0], TLCoord[1] + 1))
        self.coordSet.append((TLCoord[0] - 1, TLCoord[1] + 1))
        self.coordSet.append((TLCoord[0] - 1, TLCoord[1] + 2))

    def createLeftTwist(self, TLCoord):
        self.coordSet.append(TLCoord)
        self.coordSet.append((TLCoord[0], TLCoord[1] + 1))
        self.coordSet.append((TLCoord[0] + 1, TLCoord[1] + 1))
        self.coordSet.append((TLCoord[0] + 1, TLCoord[1] + 2))

    def createT(self, TLCoord):
        self.coordSet.append(TLCoord)
        self.coordSet.append((TLCoord[0], TLCoord[1] + 1))
        self.coordSet.append((TLCoord[0], TLCoord[1] + 2))
        self.coordSet.append((TLCoord[0] - 1, TLCoord[1] + 1))

    def moveDownPiece(self):
        lowest = self.coordSet[0][0]
        for coord in self.coordSet:
            if coord[0] > lowest:
                lowest = coord[0]
        if lowest < GRIDCOLS - 1:
            for i, coord in enumerate(self.coordSet):
                self.coordSet[i] = (coord[0] + 1, coord[1])

    def movePieceRight(self):
        farRight = self.coordSet[0][1]
        for coord in self.coordSet:
            if coord[1] > farRight:
                farRight = coord[1]
        if farRight < GRIDROWS - 1:
            for i, coord in enumerate(self.coordSet):
                self.coordSet[i] = (coord[0], coord[1] + 1)
        
    def movePieceLeft(self):
        if self.coordSet[0][1] > 0:
            for i, coord in enumerate(self.coordSet):
                self.coordSet[i] = (coord[0], coord[1] - 1)
    
    def checkMovement(self, movement, takenCoords):
        doMove = True
        if movement[0]:
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if (coord[0], coord[1] + 1) == takenCoord[0]:
                        doMove = False
            if doMove:
                self.movePieceRight()
        elif movement[1]:
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if (coord[0], coord[1] - 1) == takenCoord[0]:
                        doMove = False
            if doMove:
                self.movePieceLeft()
        elif movement[2]:
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if (coord[0] + 1, coord[1]) == takenCoord[0]:
                        doMove = False
            if doMove:
                self.moveDownPiece()
        pygame.time.delay(10)

    def rotateLine(self, takenCoords):
        oldSet = self.coordSet.copy()
        TLCoord = self.coordSet[0]
        if self.phase == 1:
            if TLCoord[0] + 2 >= GRIDCOLS:
                TLCoord = (17, TLCoord[1])
            self.coordSet[0] = (TLCoord[0] - 1, TLCoord[1] + 2)
            self.coordSet[1] = (TLCoord[0], TLCoord[1] + 2)
            self.coordSet[2] = (TLCoord[0] + 1, TLCoord[1] + 2)
            self.coordSet[3] = (TLCoord[0] + 2, TLCoord[1] + 2)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet
            self.phase += 1
        elif self.phase == 2:
            if TLCoord[1] + 1 >= GRIDROWS - 1:
                TLCoord = (TLCoord[0], 8)
            elif TLCoord[1] - 2 < 1:
                TLCoord = (TLCoord[0], 2)
            self.coordSet[0] = (TLCoord[0] + 2, TLCoord[1] - 2)
            self.coordSet[1] = (TLCoord[0] + 2, TLCoord[1] - 1)
            self.coordSet[2] = (TLCoord[0] + 2, TLCoord[1])
            self.coordSet[3] = (TLCoord[0] + 2, TLCoord[1] + 1)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet

            self.phase += 1
        elif self.phase == 3:
            if TLCoord[0] + 1 >= GRIDCOLS:
                TLCoord = (18, TLCoord[1])
            self.coordSet[0] = (TLCoord[0] - 2, TLCoord[1] + 1)
            self.coordSet[1] = (TLCoord[0] - 1, TLCoord[1] + 1)
            self.coordSet[2] = (TLCoord[0], TLCoord[1] + 1)
            self.coordSet[3] = (TLCoord[0] + 1, TLCoord[1] + 1)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet
            self.phase += 1
        elif self.phase == 4:
            if TLCoord[1] + 2 >= GRIDROWS - 1: 
                TLCoord = (TLCoord[0], 7)
            elif TLCoord[1] - 1 < 1:
                TLCoord = (TLCoord[0], 1)
            self.coordSet[0] = (TLCoord[0] + 1, TLCoord[1] - 1)
            self.coordSet[1] = (TLCoord[0] + 1, TLCoord[1])
            self.coordSet[2] = (TLCoord[0] + 1, TLCoord[1] + 1)
            self.coordSet[3] = (TLCoord[0] + 1, TLCoord[1] + 2)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet

            self.phase = 1

    def rotateLeftL(self, takenCoords):
        oldSet = self.coordSet.copy()
        TLCoord = self.coordSet[0]
        if self.phase == 1:
            if TLCoord[0] - 2 >= GRIDROWS - 1:
                TLCoord = (17, TLCoord[1])
            self.coordSet[0] = (TLCoord[0], TLCoord[1] + 1)
            self.coordSet[2] = (TLCoord[0] + 1, TLCoord[1] + 1)
            self.coordSet[1] = (TLCoord[0], TLCoord[1] + 2)
            self.coordSet[3] = (TLCoord[0] + 2, TLCoord[1] + 1)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet
            self.phase += 1
        elif self.phase == 2:
            if TLCoord[1] - 1 <= 1:
                TLCoord = (TLCoord[0], 1)
            self.coordSet[0] = (TLCoord[0] + 1, TLCoord[1] - 1)
            self.coordSet[2] = (TLCoord[0] + 1, TLCoord[1])
            self.coordSet[1] = (TLCoord[0]+ 1, TLCoord[1] + 1)
            self.coordSet[3] = (TLCoord[0] + 2, TLCoord[1] + 1)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet
            self.phase += 1
        elif self.phase == 3:
            self.coordSet[0] = (TLCoord[0] + 1, TLCoord[1])
            self.coordSet[2] = (TLCoord[0], TLCoord[1] + 1)
            self.coordSet[1] = (TLCoord[0] + 1, TLCoord[1] + 1)
            self.coordSet[3] = (TLCoord[0] - 1, TLCoord[1] + 1)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet
            self.phase += 1
        elif self.phase == 4:
            if TLCoord[1] + 1 >= GRIDROWS - 1:
                TLCoord = (TLCoord[0], 7)
            self.coordSet[0] = (TLCoord[0] - 2, TLCoord[1])
            self.coordSet[2] = (TLCoord[0] - 1, TLCoord[1] + 1)
            self.coordSet[1] = (TLCoord[0] - 1, TLCoord[1])
            self.coordSet[3] = (TLCoord[0] - 1, TLCoord[1] + 2)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet
            self.phase = 1
    
    def rotateRightL(self, takenCoords):
        oldSet = self.coordSet.copy()
        TLCoord = self.coordSet[0]
        if self.phase == 1:
            if TLCoord[0] + 1 >= GRIDCOLS - 1:
                TLCoord = (18, TLCoord[1])
            self.coordSet[0] = (TLCoord[0] - 1, TLCoord[1] + 1)
            self.coordSet[2] = (TLCoord[0], TLCoord[1] + 1)
            self.coordSet[1] = (TLCoord[0] + 1, TLCoord[1] + 1)
            self.coordSet[3] = (TLCoord[0] + 1, TLCoord[1] + 2)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet
            self.phase += 1
        elif self.phase == 2:
            if TLCoord[1] - 1 <= 1:
                TLCoord = (TLCoord[0], 1)
            self.coordSet[0] = (TLCoord[0] + 1, TLCoord[1] - 1)
            self.coordSet[2] = (TLCoord[0] + 1, TLCoord[1])
            self.coordSet[1] = (TLCoord[0]+ 1, TLCoord[1] + 1)
            self.coordSet[3] = (TLCoord[0] + 2, TLCoord[1] - 1)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet
            self.phase += 1
        elif self.phase == 3:
            self.coordSet[0] = (TLCoord[0] - 1, TLCoord[1])
            self.coordSet[2] = (TLCoord[0], TLCoord[1] + 1)
            self.coordSet[1] = (TLCoord[0] - 1, TLCoord[1] + 1)
            self.coordSet[3] = (TLCoord[0] + 1, TLCoord[1] + 1)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet
            self.phase += 1
        elif self.phase == 4:
            if TLCoord[1] + 1 >= GRIDROWS - 1:
                TLCoord = (TLCoord[0], 7)
            self.coordSet[0] = (TLCoord[0] + 1, TLCoord[1])
            self.coordSet[2] = (TLCoord[0] + 1, TLCoord[1] + 1)
            self.coordSet[1] = (TLCoord[0], TLCoord[1] + 2)
            self.coordSet[3] = (TLCoord[0] + 1, TLCoord[1] + 2)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet
            self.phase = 1

    def rotateLeftTwist(self, takenCoords):
        oldSet = self.coordSet.copy()
        TLCoord = self.coordSet[0]
        if self.phase == 1:
            if TLCoord[0] + 1 >= GRIDROWS - 1:
                TLCoord = (17, TLCoord[1])
            self.coordSet[0] = (TLCoord[0] + 1, TLCoord[1] + 1)
            self.coordSet[2] = (TLCoord[0], TLCoord[1] + 2)
            self.coordSet[1] = (TLCoord[0] + 1, TLCoord[1] + 2)
            self.coordSet[3] = (TLCoord[0] + 2, TLCoord[1] + 1)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet
            self.phase += 1
        elif self.phase == 2:
            if TLCoord[1] + 1 >= GRIDROWS - 1:
                TLCoord = (TLCoord[0], 8)
            if TLCoord[1] - 1 <= 1:
                TLCoord = (TLCoord[0], 1)
            self.coordSet[0] = (TLCoord[0], TLCoord[1] - 1)
            self.coordSet[2] = (TLCoord[0], TLCoord[1])
            self.coordSet[1] = (TLCoord[0]+ 1, TLCoord[1])
            self.coordSet[3] = (TLCoord[0] + 1, TLCoord[1] + 1)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet
            self.phase += 1
        elif self.phase == 3:
            if TLCoord[0] + 1 >= GRIDROWS - 1:
                TLCoord = (17, TLCoord[1])
            self.coordSet[0] = (TLCoord[0], TLCoord[1])
            self.coordSet[2] = (TLCoord[0], TLCoord[1] + 1)
            self.coordSet[1] = (TLCoord[0] - 1, TLCoord[1] + 1)
            self.coordSet[3] = (TLCoord[0] + 1, TLCoord[1])
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet
            self.phase += 1
        elif self.phase == 4:
            if TLCoord[1] + 1 >= GRIDROWS - 1:
                TLCoord = (TLCoord[0], 7)
            if TLCoord[1] - 1 <= 1:
                TLCoord = (TLCoord[0], 1)
            self.coordSet[0] = (TLCoord[0] - 1, TLCoord[1])
            self.coordSet[2] = (TLCoord[0] - 1, TLCoord[1] + 1)
            self.coordSet[1] = (TLCoord[0], TLCoord[1] + 1)
            self.coordSet[3] = (TLCoord[0], TLCoord[1] + 2)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet
            self.phase = 1

    def rotateRightTwist(self, takenCoords):
        oldSet = self.coordSet.copy()
        TLCoord = self.coordSet[0]
        if self.phase == 1:
            if TLCoord[0] + 1 >= GRIDCOLS - 1:
                TLCoord = (18, TLCoord[1])
            self.coordSet[0] = (TLCoord[0] - 1, TLCoord[1] + 1)
            self.coordSet[2] = (TLCoord[0], TLCoord[1] + 1)
            self.coordSet[1] = (TLCoord[0], TLCoord[1] + 2)
            self.coordSet[3] = (TLCoord[0] + 1, TLCoord[1] + 2)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet
            self.phase += 1
        elif self.phase == 2:
            if TLCoord[1] - 1 <= 1:
                TLCoord = (TLCoord[0], 1)
            self.coordSet[0] = (TLCoord[0] + 2, TLCoord[1] - 1)
            self.coordSet[2] = (TLCoord[0] + 2, TLCoord[1])
            self.coordSet[1] = (TLCoord[0]+ 1, TLCoord[1])
            self.coordSet[3] = (TLCoord[0] + 1, TLCoord[1] + 1)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet
            self.phase += 1
        elif self.phase == 3:
            self.coordSet[0] = (TLCoord[0] - 2, TLCoord[1])
            self.coordSet[2] = (TLCoord[0] - 1, TLCoord[1])
            self.coordSet[1] = (TLCoord[0] - 1, TLCoord[1] + 1)
            self.coordSet[3] = (TLCoord[0], TLCoord[1] + 1)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet
            self.phase += 1
        elif self.phase == 4:
            if TLCoord[1] + 1 >= GRIDROWS - 1:
                TLCoord = (TLCoord[0], 7)
            self.coordSet[0] = (TLCoord[0] + 1, TLCoord[1])
            self.coordSet[2] = (TLCoord[0], TLCoord[1] + 1)
            self.coordSet[1] = (TLCoord[0] + 1, TLCoord[1] + 1)
            self.coordSet[3] = (TLCoord[0], TLCoord[1] + 2)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet
            self.phase = 1

    def rotateT(self, takenCoords):
        oldSet = self.coordSet.copy()
        TLCoord = self.coordSet[0]
        if self.phase == 1:
            if TLCoord[0] + 1 >= GRIDCOLS - 1:
                TLCoord = (18, TLCoord[1])
            self.coordSet[0] = (TLCoord[0] - 1, TLCoord[1] + 1)
            self.coordSet[2] = (TLCoord[0], TLCoord[1] + 1)
            self.coordSet[1] = (TLCoord[0], TLCoord[1] + 2)
            self.coordSet[3] = (TLCoord[0] + 1, TLCoord[1] + 1)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet
            self.phase += 1
        elif self.phase == 2:
            if TLCoord[1] - 1 <= 1:
                TLCoord = (TLCoord[0], 1)
            self.coordSet[0] = (TLCoord[0] + 1, TLCoord[1] - 1)
            self.coordSet[2] = (TLCoord[0] + 1, TLCoord[1])
            self.coordSet[1] = (TLCoord[0]+ 2, TLCoord[1])
            self.coordSet[3] = (TLCoord[0] + 1, TLCoord[1] + 1)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet
            self.phase += 1
        elif self.phase == 3:
            self.coordSet[0] = (TLCoord[0], TLCoord[1])
            self.coordSet[2] = (TLCoord[0], TLCoord[1] + 1)
            self.coordSet[1] = (TLCoord[0] - 1, TLCoord[1] + 1)
            self.coordSet[3] = (TLCoord[0] + 1, TLCoord[1] + 1)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet
            self.phase += 1
        elif self.phase == 4:
            if TLCoord[1] + 1 >= GRIDROWS - 1:
                TLCoord = (TLCoord[0], 7)
            self.coordSet[0] = (TLCoord[0], TLCoord[1])
            self.coordSet[2] = (TLCoord[0], TLCoord[1] + 1)
            self.coordSet[1] = (TLCoord[0], TLCoord[1] + 2)
            self.coordSet[3] = (TLCoord[0] - 1, TLCoord[1] + 1)
            for takenCoord in takenCoords:
                for coord in self.coordSet:
                    if coord == takenCoord[0]:
                        self.coordSet = oldSet
            self.phase = 1

    def rotateBox(self, takenCoords):
        if self.phase == 4:
            self.phase = 0
        else:
            self.phase += 1

    def isBottom(self, takenCoords):
        for takenCoord in takenCoords:
            for coord in self.coordSet:
                if (coord[0] + 1, coord[1]) == takenCoord[0]:
                    return True
        lowest = self.coordSet[0][0]
        for coord in self.coordSet:
            if coord[0] > lowest:
                lowest = coord[0]
        if lowest == GRIDCOLS - 1:
            return True
        return False

    def createPiece(self):
        self.pieceFunctions[self.type](STARTPOS)
    
    def rotatePiece(self, takenCoords):
        self.rotateFunctions[self.type](takenCoords)

    def slam(self, takenCoords):
        while self.isBottom(takenCoords) == False:
            for i, coord in enumerate(self.coordSet):
                self.coordSet[i] = (coord[0] + 1, coord[1])

    def highlightPiece(self, takenCoords):
        highlightCoords = []
        oldCoordSet = self.coordSet.copy()
        while self.isBottom(takenCoords) == False:
            for i, coord in enumerate(self.coordSet):
                self.coordSet[i] = (coord[0] + 1, coord[1])
        highlightCoords = self.coordSet
        self.coordSet = oldCoordSet
        return highlightCoords

    def drawPiece(self, screen, x, y):
        if self.type == 1:
            pygame.draw.rect(screen, self.color, (x, y, SQSIZE // 1.5, SQSIZE // 1.5))
            pygame.draw.rect(screen, self.color, (x + SQSIZE // 1.5, y, SQSIZE // 1.5, SQSIZE // 1.5))
            pygame.draw.rect(screen, self.color, (x + SQSIZE // 1.5, y + SQSIZE // 1.5, SQSIZE // 1.5, SQSIZE // 1.5))
            pygame.draw.rect(screen, self.color, (x + SQSIZE // 1.5 * 2, y + SQSIZE // 1.5, SQSIZE // 1.5, SQSIZE // 1.5))
        elif self.type == 2:
            pygame.draw.rect(screen, self.color, (x, y, SQSIZE // 1.5, SQSIZE // 1.5))
            pygame.draw.rect(screen, self.color, (x, y + SQSIZE // 1.5, SQSIZE // 1.5, SQSIZE // 1.5))
            pygame.draw.rect(screen, self.color, (x + SQSIZE // 1.5, y + SQSIZE // 1.5, SQSIZE // 1.5, SQSIZE // 1.5))
            pygame.draw.rect(screen, self.color, (x + SQSIZE // 1.5 * 2, y + SQSIZE // 1.5, SQSIZE // 1.5, SQSIZE // 1.5))
        elif self.type == 3:
            pygame.draw.rect(screen, self.color, (x, y, SQSIZE // 1.5, SQSIZE // 1.5))
            pygame.draw.rect(screen, self.color, (x + SQSIZE // 1.5, y, SQSIZE // 1.5, SQSIZE // 1.5))
            pygame.draw.rect(screen, self.color, (x + SQSIZE // 1.5, y - SQSIZE // 1.5, SQSIZE // 1.5, SQSIZE // 1.5))
            pygame.draw.rect(screen, self.color, (x + SQSIZE // 1.5 * 2, y - SQSIZE // 1.5, SQSIZE // 1.5, SQSIZE // 1.5))
        elif self.type == 4:
            pygame.draw.rect(screen, self.color, (x, y, SQSIZE // 1.5, SQSIZE // 1.5))
            pygame.draw.rect(screen, self.color, (x + SQSIZE // 1.5, y, SQSIZE // 1.5, SQSIZE // 1.5))
            pygame.draw.rect(screen, self.color, (x + SQSIZE // 1.5 * 2, y, SQSIZE // 1.5, SQSIZE // 1.5))
            pygame.draw.rect(screen, self.color, (x + SQSIZE // 1.5 * 2, y - SQSIZE // 1.5, SQSIZE // 1.5, SQSIZE // 1.5))
        elif self.type == 5:
            pygame.draw.rect(screen, self.color, (x, y, SQSIZE // 1.5, SQSIZE // 1.5))
            pygame.draw.rect(screen, self.color, (x + SQSIZE // 1.5, y, SQSIZE // 1.5, SQSIZE // 1.5))
            pygame.draw.rect(screen, self.color, (x + SQSIZE // 1.5, y + SQSIZE // 1.5, SQSIZE // 1.5, SQSIZE // 1.5))
            pygame.draw.rect(screen, self.color, (x, y + SQSIZE // 1.5, SQSIZE // 1.5, SQSIZE // 1.5))
        elif self.type == 6:
            pygame.draw.rect(screen, self.color, (x, y, SQSIZE // 1.5, SQSIZE // 1.5))
            pygame.draw.rect(screen, self.color, (x + SQSIZE // 1.5, y, SQSIZE // 1.5, SQSIZE // 1.5))
            pygame.draw.rect(screen, self.color, (x + (SQSIZE // 1.5) * 2, y, SQSIZE // 1.5, SQSIZE // 1.5))
            pygame.draw.rect(screen, self.color, (x + SQSIZE // 1.5, y - SQSIZE // 1.5, SQSIZE // 1.5, SQSIZE // 1.5))
        elif self.type == 7:
            pygame.draw.rect(screen, self.color, (x, y, SQSIZE // 1.5, SQSIZE // 1.5))
            pygame.draw.rect(screen, self.color, (x + SQSIZE // 1.5, y, SQSIZE // 1.5, SQSIZE // 1.5))
            pygame.draw.rect(screen, self.color, (x + SQSIZE // 1.5 * 2, y, SQSIZE // 1.5, SQSIZE // 1.5))
            pygame.draw.rect(screen, self.color, (x + SQSIZE // 1.5 * 3, y, SQSIZE // 1.5, SQSIZE // 1.5))


pygame.quit()