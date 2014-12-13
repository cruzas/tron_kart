"""
This file contains the tron food class.
"""

import pygame
import random


class TFood:
    
    """Simple class to represent object of type TFood"""

    # static variable that keeps track of the type of powers-up that a TFood can give
    powers = ["SPEED", "SIZE"]
    
    def __init__(self, surface, img_path, power, size=(30, 30), name=''):
        """ WRITE HERE THE DOCS FOR THIS FUNCTION!!! """
        if power not in TFood.powers:
            raise ValueError('power has not a correct value')
        
        self.name = name
        self.power = power # setting the type of power
        # coordinates of the TFood object in the surface
        self.x = 0
        self.y = 0
        self.surface = surface
        self.size = size
        self.width = size[0]
        self.height = size[1]
        
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
    #
    
    def update_rect(self):
        """ WRITE HERE THE DOCS FOR THIS FUNCTION!!! """
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
    #
    
    def generate(self):
        """ WRITE HERE THE DOCS FOR THIS FUNCTION!!! """
        self.x = round(random.randrange(0, self.surface.get_rect()[2] - self.width))
        self.y = round(random.randrange(0, self.surface.get_rect()[3] - self.height))
        self.update_rect()
    #
    
    def appear(self):
        """ WRITE HERE THE DOCS FOR THIS FUNCTION!!! """
        self.surface.blit(self.image, (self.x, self.y))
    #
    
# end TFood
