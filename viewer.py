import pygame
import numpy as np
import math

class View():
    '''
    Aggregating and wrapping pygame methods and properties into a viewer class.
    '''
    def __init__(self, rows, colums, size):
        pygame.init()
        self.columns = colums
        self.rows = rows
        self.size = size
        self.radius = int(size/2 -8) # int parsing because of divison      
        self.screen = pygame.display.set_mode((size*(rows+1), size*colums))
        self.blue = (0, 0, 255)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)           

    def draw_game_board(self):
        '''
        Input: Array of form [rows,colums] which contains the current board state.
        Draws the current board state to the view
        '''
        for i in range(self.columns):
            for o in range(self.rows):
                pygame.draw.rect(self.screen, self.blue, (i * self.size, o * self.size + self.size,
                                     self.size, self.size))
                pygame.draw.circle(self.screen, self.white, (int(i*self.size + self.size/2),
                                     int(o * self.size + self.size + self.size/2)), self.radius)
        pygame.display.update()



inst = View(6,7,100)
inst.draw_game_board()

pygame.display.update()

while True:
    pass


class Board():
    '''
    Data structure for the game board
    '''
