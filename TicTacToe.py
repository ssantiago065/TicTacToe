import sys
import pygame
import random
import copy
import numpy as np
import time

from constants import * 

#Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("UNBEATABLE TIC TAC TOE")


#Function that writes any text on the screen with a preset for font size and color
def draw_text(screen, text, position, font_size=30, color=(255, 255, 255)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

class Board:

    """
    Represents the Tic Tac Toe board and its state.

    Attributes:
        squares (np.ndarray): A 2D array representing the board state. 
                              0 means empty, 1 means Player 1 (cross), and 2 means Player 2 (circle).
        marked_squares (int): The count of marked squares on the board.

    Methods:
        final_state(show=False): Determines if the game has ended and identifies the winner.
        mark_square(row, column, player): Marks a square with the given player's symbol.
        square_empty(row, column): Checks if a square is empty.
        get_empty_squares(): Returns a list of all empty squares on the board.
        is_full(): Checks if the board is completely filled.
        is_empty(): Checks if the board is completely empty.
    """
    
    def __init__(self):
        self.squares = np.zeros( (ROWS,COLUMNS) )
        self.empty_squares = self.squares
        self.marked_squares = 0

    def final_state(self, show=False):
        
        #Vertical wins
        for column in range(COLUMNS):
            if self.squares[0][column] == self.squares[1][column] == self.squares[2][column] != 0:
                if show:
                    color = CIRCLE if self.squares[0][column] == 2 else LINE
                    start = (column * SQUARESIZE + SQUARESIZE // 2, OFFSET)
                    finish = (column * SQUARESIZE + SQUARESIZE // 2, HEIGHT - OFFSET)
                    pygame.draw.line(screen, color, start, finish, LINEWIDTH)
                return self.squares[0][column]

        #Horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRCLE if self.squares[row][0] == 2 else LINE
                    start = (OFFSET, row * SQUARESIZE + SQUARESIZE // 2)
                    finish = (WIDTH - OFFSET, row * SQUARESIZE + SQUARESIZE // 2)
                    pygame.draw.line(screen, color, start, finish, LINEWIDTH)
                return self.squares[row][0]

        #Descending diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRCLE if self.squares[1][1] == 2 else LINE
                start = (OFFSET - 20, OFFSET - 20)
                finish = (WIDTH - OFFSET + 20, HEIGHT - OFFSET + 20)
                pygame.draw.line(screen, color, start, finish, LINEWIDTH)
            return self.squares[1][1]
        
        #Ascending diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRCLE if self.squares[1][1] == 2 else LINE
                start = (OFFSET - 20, HEIGHT - OFFSET + 20)
                finish = (WIDTH - OFFSET + 20, OFFSET - 20)
                pygame.draw.line(screen, color, start, finish, LINEWIDTH)
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

    """
    Implements the Minimax algorithm with alpha-beta pruning for Tic Tac Toe.

    Attributes:
        mode (int): The game mode. 0 for random moves, 1 for Minimax algorithm.
        player (int): The player controlled by the AI (always Player 2).

    Methods:
        rand(board): Generates a random move from the available empty squares.
        minimax(board, maximizing, alpha, beta): Applies the Minimax algorithm to find the optimal move.
        eval(main_board): Evaluates the best move based on the current mode (random or Minimax).
    """
    
    def __init__(self, mode=1, player=2):
        self.mode = mode
        self.player = player

    def rand(self,board):
        empty_squares = board.get_empty_squares()
        index = random.randrange(0, len(empty_squares))

        return empty_squares[index]
    
    def minimax(self, board, maximizing, alpha, beta):
        #Terminal state
        state = board.final_state()

        #Player 1 wins
        if state == 1:
            return 1, None
        
        #Player 2 wins
        elif state == 2:
            return -1, None
        
        #Board is full (draw)
        elif board.is_full():
            return 0, None
        
        if maximizing:
            max_eval = float("-inf")
            best_move = None
            empty_squares = board.get_empty_squares()

            for (row,column) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row,column, 1)
                eval = self.minimax(temp_board, False, alpha, beta)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row,column)

                alpha = max(eval, alpha)
                if beta <= alpha:
                    break
            
            return max_eval, best_move
        
        else:
            min_eval = float("inf")
            best_move = None
            empty_squares = board.get_empty_squares()

            for (row,column) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row,column, 2)
                eval = self.minimax(temp_board, True, alpha, beta)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row,column)

                beta = min(eval, beta)
                if beta <= alpha:
                    break
            
            return min_eval, best_move
                
        
    
    def eval(self,main_board):
        if self.mode == 0:
            #random
            start = time.time()
            eval = "Random"
            move = self.rand(main_board)
            end = time.time()
            execution_time = (end-start) * 10**3

        else:
            start = time.time()
            #minimax
            eval, move = self.minimax(main_board,False, float("-inf"), float("inf"))
            end = time.time()
            execution_time = (end-start) * 10**3

        print(f"Best move is {move} with evaluation of {eval} and an execution time of {execution_time}, ms")

        return move
    
class Game:

    """
    Manages the flow and logic of the Tic Tac Toe game.

    Attributes:
        board (Board): The current game board.
        minimax (MiniMax): The Minimax algorithm instance for AI moves.
        player (int): The current player's turn. 1 for Player 1 (cross), 2 for Player 2 (circle).
        gamemode (str): The current game mode, either "pvp" or "minimax".
        running (bool): Indicates if the game is currently active.

    Methods:
        show_lines(): Draws the grid lines on the screen.
        change_turn(): Alternates the turn between Player 1 and Player 2.
        draw_fig(row, column): Draws the player's figure (cross or circle) on the board.
        make_move(row, column): Executes a move by marking the square and changing the turn.
        change_gamemode(): Toggles the game mode between "pvp" and "minimax".
        reset(): Resets the game state to start a new game.
        is_over(): Checks if the game has ended and displays the winner or draw.
    """
    
    def __init__(self):
        self.board = Board()
        self.minimax = MiniMax()
        self.player = 1 # 1 - cross 2 - circle
        self.gamemode = "minimax" #pvp or minimax
        self.running = True
        screen.fill(BACKGROUND)
        draw_text(screen, "Press 'G' to toggle modes (PvP/Minimax(default))", (20, 20))
        draw_text(screen, "Press 'R' to reset the game", (20, 60))
        draw_text(screen, "Press '0' for random mode, '1' for Minimax", (20, 100))
        pygame.display.update()
        pygame.time.delay(6000)  # Show message for 6 seconds before starting
        screen.fill(BACKGROUND)
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
    
    def make_move(self, row, column):
        self.board.mark_square(row,column,self.player)
        self.draw_fig(row, column)
        self.change_turn()

    def change_gamemode(self):
        self.gamemode = "minimax" if self.gamemode == "pvp" else "pvp"

    def reset(self):
        self.__init__()

    def is_over(self):
        winner = self.board.final_state(show=True)
        if winner == 1:
            draw_text(screen, "Player 1 Wins!", (WIDTH // 2 - OFFSET, HEIGHT // 2))
        elif winner == 2:
            draw_text(screen, "Player 2 Wins!", (WIDTH // 2 - OFFSET, HEIGHT // 2))
        elif self.board.is_full():
            draw_text(screen, "It's a Draw!", (WIDTH // 2 - OFFSET, HEIGHT // 2))

        pygame.display.update()
        return winner != 0 or self.board.is_full()




    

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

            if event.type == pygame.KEYDOWN:
                #g - change mode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                #r - reset game
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    minimax = game.minimax

                #0 - random mode
                if event.key == pygame.K_0:
                    minimax.mode = 0

                if event.key == pygame.K_1:
                #1 - minimax mode
                    minimax.mode = 1

            if event.type == pygame.MOUSEBUTTONDOWN :
                column, row = event.pos
                row = row // SQUARESIZE
                column = column // SQUARESIZE
                
                if board.square_empty(row,column) and game.running:
                    game.make_move(row, column)

                    if game.is_over():
                        game.running = False

        if game.gamemode == "minimax" and game.player == minimax.player and game.running:
            pygame.display.update()


            row, column = minimax.eval(board)
            game.make_move(row, column)

            if game.is_over():
                game.running = False

        pygame.display.update()

main()