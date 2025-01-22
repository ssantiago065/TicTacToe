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
    
    def __init__(self):
        self.squares = np.zeros( (ROWS,COLUMNS) )

    def mark_square(self, row, column, player):
        self.squares[row][column] = player 


class MiniMax:
    pass

class Game:
    
    def __init__(self):
        self.board = Board()
        self.player = 1
        self.show_lines()

    def show_lines(self):
        #Vertical
        pygame.draw.line(screen, LINE, (SQUARESIZE,0), (SQUARESIZE,HEIGHT), LINEWIDTH)
        pygame.draw.line(screen, LINE, (WIDTH-SQUARESIZE,0), (WIDTH-SQUARESIZE,HEIGHT), LINEWIDTH)

        #Horizontal
        pygame.draw.line(screen, LINE, (0,SQUARESIZE), (WIDTH,SQUARESIZE), LINEWIDTH)
        pygame.draw.line(screen, LINE, (0,HEIGHT-SQUARESIZE), (WIDTH,HEIGHT-SQUARESIZE), LINEWIDTH)
    

def main():
    
    game = Game()

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

main()