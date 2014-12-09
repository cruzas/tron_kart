'''
Created on Dec 6, 2014

@author: Nelson Dos Santos
'''

import pygame
from game import Game
import colors

if __name__ == '__main__':
    pygame.init()

    res = (900, 700)
    title = 'Notorcycle'
    game1 = Game(res, title, colors.BLACK, 30)
    
    pygame.quit()
    quit()
