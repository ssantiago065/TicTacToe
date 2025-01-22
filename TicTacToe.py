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

    def is_empty(self, row, column):
        return self.squares[row][column] == 0


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

    def change_turn(self):
        self.player = self.player % 2 + 1

    def draw_fig(self, row, column):
        if self.player == 1:
            #Cross
            #Descending Line
            start_desc = (column * SQUARESIZE + OFFSET, row * SQUARESIZE + OFFSET)
            end_desc = (column * SQUARESIZE + SQUARESIZE - OFFSET, row * SQUARESIZE + SQUARESIZE - OFFSET)
            pygame.draw.line(screen, CROSS, start_desc, end_desc, CROSSWIDTH)

            #Ascending Line
            start_asc = (column * SQUARESIZE + OFFSET, row * SQUARESIZE + SQUARESIZE - OFFSET)
            end_asc = (column * SQUARESIZE + SQUARESIZE - OFFSET, row * SQUARESIZE + OFFSET)
            pygame.draw.line(screen, CROSS, start_asc, end_asc, CROSSWIDTH)

        elif self.player == 2:
            #Circle
            center = (column * SQUARESIZE + SQUARESIZE // 2, row * SQUARESIZE + SQUARESIZE // 2)
            pygame.draw.circle(screen, CIRCLE, center, RADIUS, CIRCLEWIDTH)
    

def main():
    
    game = Game()
    board = game.board

    #Game loop
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                column, row = event.pos
                row = row // SQUARESIZE
                column = column // SQUARESIZE
                
                if board.is_empty(row,column):
                    board.mark_square(row,column,game.player)
                    game.draw_fig(row, column)
                    game.change_turn()
                    

                

        pygame.display.update()

main()