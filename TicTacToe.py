import sys
import pygame
import random
import copy
import numpy as np

from constants import * 

#Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("UNBEATABLE TIC TAC TOE")
screen.fill(BACKGROUND)

class Board:
    pass

class MiniMax:
    pass

class Game:
    pass

def main():
    pass

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

main()