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
        self.empty_squares = self.squares
        self.marked_squares = 0

    def final_state(self):
        
        #Vertical wins
        for column in range(COLUMNS):
            if self.squares[0][column] == self.squares[1][column] == self.squares[2][column] != 0:
                return self.squares[0][column]

        #Horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]

        #Descending diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[1][1]
        
        #Ascending diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return self.squares[1][1]
        
        return 0

    def mark_square(self, row, column, player):
        self.squares[row][column] = player 
        self.marked_squares += 1

    def square_empty(self, row, column):
        return self.squares[row][column] == 0
    
    def get_empty_squares(self):
        empty_squares = []
        for row in range(ROWS):
            for column in range(COLUMNS):
                if self.square_empty(row, column):
                    empty_squares.append( (row,column) )

        return empty_squares
    
    def is_full(self):
        return self.marked_squares == 9
    
    def is_empty(self):
        return self.marked_squares == 0
    

    

class MiniMax:
    
    def __init__(self,mode=0,player=2):
        self.mode = mode
        self.player = player

    def rand(self,board):
        empty_squares = board.get_empty_squares()
        index = random.randrange(0, len(empty_squares))

        return empty_squares[index]
    
    def eval(self,main_board):
        if self.mode == 0:
            #random
            move = self.rand(main_board)

        else:
            #minimax
            pass

        return move
    
class Game:
    
    def __init__(self):
        self.board = Board()
        self.minimax = MiniMax()
        self.player = 1 # 1 - cross 2 - circle
        self.gamemode = "minimax" #pvp or minimax
        self.running = True
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
    minimax = game.minimax

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
                
                if board.square_empty(row,column):
                    board.mark_square(row,column,game.player)
                    game.draw_fig(row, column)
                    game.change_turn()
            
        if game.gamemode == "minimax" and game.player == minimax.player:
            pygame.display.update()

            row, column = minimax.eval(board)
            board.mark_square(row,column,minimax.player)
            game.draw_fig(row, column)
            game.change_turn()
            

                    

                

        pygame.display.update()

main()