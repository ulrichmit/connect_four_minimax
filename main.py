import numpy as np
import math
import pygame
import sys

# Pygame initialization
pygame.init()

# Graphics variable
rows = 6
columns = 7
size = 100
radius = int(size/2 -8) # int parsing because of divison
blue = (0,0,255)
black = (0,0,0) 
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (0, 255, 0)
winning_font = pygame.font.SysFont("monospace", 75)

# Game variables
game_over = False
move_count = 0
selection = 0


screen_size = (size*(rows+1), size*columns)
screen = pygame.display.set_mode(screen_size)

# Functions
def create_game_board():
    return np.zeros((rows,columns))

def print_board():
    print(np.flip(board, axis=0))

def place_stone(board, col, row, stone):
    board[row][col] = stone

def column_possible(board, col):
    return board[rows-1][col] == 0

def get_row_position(board, col):
    for i in range(rows):
        if board[i][col] == 0:
            return i

def check_win(boad, stone):
    '''
    Method for checking all possible win postions.
    '''
    # vertical
    for c in range(columns):
        for r in range(rows-2):
            if (board[r][c] == stone and board[r+1][c] == stone
                 and board[r+2][c] == stone and board[r+3][c] == stone):
                 return True

    # horizontal
    for c in range(columns-3):
        for r in range(rows):
            if (board[r][c] == stone and board[r][c+1] == stone
                 and board[r][c+2] == stone and board[r][c+3] == stone):
                 return True

    # diagonal right to left up
    for c in range(columns-3):
        for r in range(rows-2):
            if (board[r][c] == stone and board[r+1][c+1] == stone
                 and board[r+2][c+2] == stone and board[r+3][c+3] == stone):
                 return True
    
    # diagonal left to right up
    for c in range(columns-3):
        for r in range(3, rows):
            if (board[r][c] == stone and board[r-1][c+1] == stone
                 and board[r-2][c+2] == stone and board[r-3][c+3] == stone):
                 return True

def draw_board(game_board):
    # Build background
    for c in range(columns):
        for r in range(rows):
            pygame.draw.rect(screen, blue, (c*size, r*size + size, size, size))            
            pygame.draw.circle(screen, white, (int(c*size +size/2), int(r*size+size+size/2)),radius)
    
    # Fill board    
    for c in range(columns):
        for r in range(rows):            
            if board[r][c] == 1:
                pygame.draw.circle(screen, red, (int(c*size + size/2), (rows+1)*size-int(r*size+size/2)),radius)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, yellow, (int(c*size + size/2), (rows+1)*size-int(r*size+size/2)),radius)            
    pygame.display.update()


board = create_game_board()
# print_board()
draw_board(board)


# Game Loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONUP:            
            # Player 1 Move
            if move_count == 0:
                col = int(math.floor(event.pos[0]/size))            
                
                if column_possible(board, col):
                    place_stone(board, col, get_row_position(board, col), 1)

                if check_win(board, 1):
                    game_over = True
                    win_message = winning_font.render("Player 1 won!",1,red)
                    screen.blit(win_message, (30,5))

            #Player 2 move
            else: 
                col = int(math.floor(event.pos[0]/size))                       

                if column_possible(board, col):
                    place_stone(board, col, get_row_position(board, col), 2)

                if check_win(board, 2):
                    game_over = True
                    win_message = winning_font.render("Player 1 won!",1,red)
                    screen.blit(win_message, (30,5))
            
            # change move count if move was made
            move_count += 1
            move_count = move_count % 2
            #print_board()
            draw_board(board)

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0,0, columns*size, size))
            x_pos = event.pos[0]
            if move_count == 0:
                pygame.draw.circle(screen, red, (x_pos, int(size/2)), radius)
            else:
                pygame.draw.circle(screen, yellow, (x_pos, int(size/2)), radius)

            pygame.display.update()


    if game_over:
        pygame.time.wait(3000)