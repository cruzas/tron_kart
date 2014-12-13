'''
Created on Dec 7, 2014

@author: Nelson Dos Santos
'''

import pygame
from colors import *


class Person(object):
    '''
    classdocs
    '''

    def __init__(self, surface, name, img, size, pos, step=2, sounds=[]):
        '''
        Constructor
        '''
        if type(surface) != pygame.Surface:
            raise TypeError('surface is not a pygame.Surface')
        if type(name) != str:
            raise TypeError('name is not a str')
        if type(img) != str:
            raise TypeError('img is not a str')
        if type(size) != tuple or len(size) != 2:
            raise TypeError('incorrect value for size')
        if type(pos) != tuple or len(pos) != 2:
            raise TypeError('incorrect format for pos')
        for c in pos:
            if type(c) != int:
                raise TypeError('position coordinate is not an int')
        if type(step) != int or step < 0:
            raise TypeError('incorrect value for step')
        if type(sounds) != list:
            raise TypeError('sounds is not a list')
        for s in sounds:
            if type(s) != str:
                raise TypeError('a sound path is not a str')
        #
        
        self.surface = surface
        self.name = name
        self.img = img
        self.size = size
        self.step = step
        self.width = self.size[0]
        self.height = self.size[1]
        self.sounds = sounds
        
        # Keeps track if you are turned left, right, up or down.
        self.direction = [True, False, False, False]
        
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        
        # offset to add to x and y when moving
        self.x_speed = 0
        self.y_speed = 0
        
        # setting up the image for the player
        self.image = pygame.image.load(self.img).convert()
        self.image.set_colorkey(BLACK) # set the color passed as parameter to transparent.
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        
        pygame.display.update()
    #
    def reset_direction(self):
        self.direction.clear()
        for _ in range(4):
            self.direction.append(False)    
    #
    
    def set_direction(self, new_dir):
        '''0=North, 1=South, 2=Left, 3=Right'''
        if type(new_dir) != int:
            raise TypeError('new_dir is not an int')
        if new_dir >= 0 and new_dir <= 3:
            if new_dir == 0:    
                if self.direction[0]:
                    self.turn(0)
                elif self.direction[1]:
                    self.turn(180)
                elif self.direction[2]:
                    self.turn(-90)                            
                elif self.direction[3]:
                    self.turn(90)
                self.reset_direction()
                self.direction[0] = True

            elif new_dir == 1:
                if self.direction[0]:
                    self.turn(180)
                elif self.direction[1]:
                    self.turn(0)
                elif self.direction[2]:
                    self.turn(90)
                elif self.direction[3]:
                    self.turn(-90)
                    
                self.reset_direction()
                self.direction[1] = True
                
            elif new_dir == 2:
                if self.direction[0]:
                    self.turn(90)
                elif self.direction[1]:
                    self.turn(-90)
                elif self.direction[2]:
                    self.turn(0)
                elif self.direction[3]:
                    self.turn(180)
                    
                self.reset_direction()
                self.direction[2] = True
            
            elif new_dir == 3:
                if self.direction[0]:
                    self.turn(-90)
                elif self.direction[1]:
                    self.turn(90)
                elif self.direction[2]:
                    self.turn(180)
                elif self.direction[3]:
                    self.turn(0)
                    
                self.reset_direction()
                self.direction[3] = True
    #    
    
    def appear(self):
        self.surface.blit(self.image, self.rect)
    #
    
    # changes x_change or y_change
    def move(self):
        if self.direction[0]:
            self.y_speed -= self.step
        elif self.direction[1]:
            self.y_speed += self.step
        elif self.direction[2]:
            self.x_speed -= self.step                          
        elif self.direction[3]:
            self.x_speed += self.step
    #
    
    # changes x_change or y_change
    def brake(self):
        if self.y_speed > 0:  # when self.y is 0, no change is made to it
            self.y_speed -= int(self.step / 2)
        elif self.y_speed < 0:
            self.y_speed += int(self.step / 2)
            
        if self.x_speed > 0: # when self.y is 0, no change is made to it
            self.x_speed -= int(self.step / 2)
        elif self.x_speed < 0:
            self.x_speed += int(self.step / 2)
    #
    
    def goto(self, x, y):
        if type(x) != int or type(y) != int:
            raise TypeError('x or y are not of type int')
        self.x = x
        self.y = y
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
    #

    def goto_initial_pos(self):
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
    #

    def set_step(self, step):
        if type(step) != int:
            raise TypeError('step is not an int')
        if step > 0:
            self.step = step
    
    
    def crashing(self):
        """Returns true if this person touching self.surface"""
        if (self.x >= self.surface.get_size()[0] - self.width) or \
        (self.x <= 0) or (self.y <= 0) or \
        (self.y >= self.surface.get_size()[1] - self.height):
            return True
        else:
            return False
    #
    
    def turn(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)
    
    
