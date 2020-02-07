import numpy as np
import math
import pygame
import sys
import random

# Graphics
rows = 6
columns = 7
size = 100
radius = int(size/2 -8)
brown = (222,184,135)
black = (0,0,0) 
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (0, 255, 0)

# Game variables
PLAYER = 0
AI = 1
player_stone = 1
ai_stone = 2
available = 0
part_length = 4
game_over = False
move_count = 0

# Pygame initialization
pygame.init()
screen_size = (size*(rows+1), size*columns)
screen = pygame.display.set_mode(screen_size)

# Functions
def create_game_board():
    '''
    Returns a board datastructure.
    '''
    return np.zeros((rows,columns))

def print_board(board):
    '''
    Prints the current game board to the terminal.
    '''
    print(np.flip(board, axis=0))

def place_stone(board, row, col, stone):
    '''
    Places a stone on the given position in the game board.
    '''
    board[row][col] = stone

def column_possible(board, col):
    '''
    Returns a bool if a stone can be places in the col column.
    '''
    return board[rows-1][col] == 0

def get_possible_columns(board):
    '''
    Returns an array of all possible locations to place a stone.
    Where the columns are not full.
    '''
    possible_locations = []
    for c in range(columns):
        if column_possible(board, c):
            possible_locations.append(c)
    return possible_locations
        
def get_row_position(board, col):
    '''
    Returns the next available row position in the column col.
    '''
    for i in range(rows):
        if board[i][col] == 0:
            return i

def check_win(boad, stone):
    '''
    Checks all possible winnig postions. (4 stones in a row)
    Returns true if player of stone won.
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

def eval_part(part, stone):
    '''
    Returns a value based on the number of stones in the givven part.
    The more sotones and available positions the better the score.
    If the enemy has already a 3 in a row and the fourth is available - Give negative reward!
    '''
    score = 0
    enemy_stone = player_stone
    if stone == player_stone:
        enemy_stone = ai_stone

    # Positives scores of the current part
    if part.count(stone) == 4:
        score += 100
    elif part.count(stone) == 3 and part.count(available) == 1:
        score += 30
    elif part.count(stone) == 2 and part.count(available) == 2:
        score += 5
    
    # Enemy has 3 in a row - negative score - all other moves are better
    if part.count(enemy_stone) == 3 and part.count(available) == 1:
        score -= 12
    
    return score

def board_heuristics(board, stone):
    '''
    Evaluates the score of the givven board for the given player
    Using list comprehensions to check parts of 4 neigbouring spots
    Part evaluaiton is done in eval_part function
    '''
    score = 0
    # scoring the center postions since from them better chances arise
    center_arr = [int(i) for i in list(board[:,columns//2])]
    num_center = center_arr.count(stone)
    #score += num_center * 1

    # horizontal
    for r in range(rows):
        row_arr = [int(i) for i in list(board[r,:])] # whole row
        for c in range(columns-3):
            part = row_arr[c:c+part_length]
            score += eval_part(part, stone)

    # vertical
    for c in range(columns):
        col_arr = [int(i) for i in list(board[:,c])] # whole column
        for r in range(rows-2):
            part = col_arr[r:r+part_length]
            score += eval_part(part, stone)

    # diagonal left to right up
    for r in range(rows-3):
        for c in range(columns-3):
            part = [board[r+i][c+i] for i in range(part_length)]
            score += eval_part(part, stone)
            
    # diagonal left to right down
    for r in range(rows-3):
        for c in range(columns-3):
            part = [board[r+3-i][c+i] for i in range(part_length)]
            score += eval_part(part, stone)            

    return score

def terminal_node(board):
    '''
    Returns true if board is winning for either the Huma or AI or the board is full
    '''
    return len(get_possible_columns(board)) == 0 or check_win(board, player_stone) or check_win(board, ai_stone)


def minimax(board, depth, alpha, beta, maximizing_player):
    '''
    Minimax implementation
    pseudocode: https://en.wikipedia.org/wiki/Minimax
    pseudocode alpha, beta pruning: https://en.wikipedia.org/wiki/Alpha–beta_pruning
    With alpha beta, additional to getting the max value we are evaluatin alpha, beta
    https://www.youtube.com/watch?v=l-hh51ncgDI
    '''
    is_terminal = terminal_node(board)
    possible_columns = get_possible_columns(board)

    if is_terminal:            
        if check_win(board, ai_stone):
            return (None, math.inf) # AI won
        elif check_win(board, player_stone):
            return (None, -math.inf) # Player won
        else:
            return (None, 0) # draw         
    elif depth == 0:
        return (None, board_heuristics(board, ai_stone)) # Last board in the branch - return heuristic

    if maximizing_player:
        value = -math.inf
        column = random.choice(possible_columns)
        # Build each child just in time with placing a stone in each possible column
        for col in possible_columns:
            row = get_row_position(board,col)
            current_board = board.copy()
            place_stone(current_board, row, col, ai_stone)
            current_score = minimax(current_board, depth-1, alpha, beta, False)[1] # recursive call
            if current_score > value:
                value = current_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta: # Pruning - Already better option available
                break 
        return (column, value)

    else:
        value = math.inf
        column = random.choice(possible_columns)
        # Build each child just in time with placing a stone in each possible column
        for col in possible_columns:
            row = get_row_position(board,col)
            current_board = board.copy()
            place_stone(current_board, row, col, player_stone)
            current_score = minimax(current_board, depth-1, alpha, beta, True)[1] # recursive call
            if current_score < value:
                value = current_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break # Pruning - Already better option available
        return (column, value)


def draw_board(board):
    '''
    Draws the current board to the pygame screen.
    '''
    # Build background
    for c in range(columns):
        for r in range(rows):
            pygame.draw.rect(screen, brown, (c*size, r*size + size, size, size))            
            pygame.draw.circle(screen, white, (int(c*size +size/2), int(r*size+size+size/2)),radius)
    
    # Fill board    
    for c in range(columns):
        for r in range(rows):            
            if board[r][c] == player_stone:
                pygame.draw.circle(screen, red, (int(c*size + size/2), (rows+1)*size-int(r*size+size/2)),radius)
            elif board[r][c] == ai_stone:
                pygame.draw.circle(screen, yellow, (int(c*size + size/2), (rows+1)*size-int(r*size+size/2)),radius)            
    pygame.display.update()


board = create_game_board()
draw_board(board)
move_count = AI

# Game Loop
while not game_over:
    # Pygame event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0,0, columns*size, size))
            x_pos = event.pos[0]
            if move_count == 0:
                pygame.draw.circle(screen, red, (x_pos, int(size/2)), radius)            
            pygame.display.update()
          
        if event.type == pygame.MOUSEBUTTONUP:            
            pygame.draw.rect(screen, black, (0,0, columns*size, size))
            
            # Player Move
            if move_count == PLAYER:
                col = int(math.floor(event.pos[0]/size))            
                
                if column_possible(board, col):
                    place_stone(board, get_row_position(board, col), col, player_stone)

                    if check_win(board, player_stone):
                        game_over = True
                        print("----------------------")
                        print("HUMANITY won!!")
                        print("----------------------")
                    
                    move_count += 1
                    move_count = move_count % 2
                    draw_board(board)

    # AI move
    if move_count == AI and not game_over:
        col, score = minimax(board, 4, -math.inf, math.inf, True) # Initial call, Worst possible alpha, beta

        if column_possible(board, col):            
            place_stone(board, get_row_position(board, col) , col, ai_stone)

            if check_win(board, ai_stone):
                game_over = True
                print("----------------------")
                print("AI won - We're doomed!!") 
                print("----------------------")              

            move_count += 1
            move_count = move_count % 2
            draw_board(board)

print_board(board)







# Discarded function
def choose_best_move(board, stone):
    '''
    Does a move on every possible column and returns the column
    position best one based on the result of the heuristics
    '''
    possible_columns = get_possible_columns(board)
    max_score = -math.inf
    max_column = random.choice(possible_columns)
    for c in possible_columns:
        r = get_row_position(board, c)
        board_copy = board.copy() # A new memory location has to be created
        place_stone(board_copy, r, c, stone)
        score = board_heuristics(board_copy, stone) # Get heuristic on the new board
        if score > max_score:
            max_score = score
            max_column = c
    return max_column