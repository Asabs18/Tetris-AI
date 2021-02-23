import pygame, copy, random
from Piece import Piece

pygame.init()

def setMovement(event, change, movement):
    if event.key == pygame.K_RIGHT:
        movement[0] = change
    elif event.key == pygame.K_LEFT:
        movement[1] = change
    elif event.key == pygame.K_DOWN:
        movement[2] = change

def drawText(screen, text, ftSize, coord):
    font = pygame.font.SysFont("Arial", ftSize)
    textObject = font.render(text, 0, pygame.Color('Black'))
    screen.blit(textObject, (coord[0] - textObject.get_width(), coord[1], textObject.get_width(), textObject.get_height()))

pygame.quit()