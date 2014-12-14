"""
This file contains the tron motorcycle class.
"""

import pygame
from src.tfood import TFood
from src.ttimer import TTimer


class TMoto:
    """Main class containing the TMoto for this game."""

    # static variable
    
    STATUS = [0, 1, 2] # collision status: 0=NO, 1=YES, 2=BOTH
    MAX_LIVES = 3

    def __init__(self, surface, name, lives, img_path, pos, piece_color, size=(30, 30), piece_size=(4, 4), direction='', length=60):
        """ WRITE HERE THE DOCS FOR THIS FUNCTION!!! """
        self.timer = TTimer(100) # 100 is the amount of "time" that has to pass
        self.explosion_sound = pygame.mixer.Sound('src/sounds/explosion.aiff')

        self.name = name
        self.surface = surface
        self.direction = direction
        self.previous_direction = self.direction
        self.img_path = img_path
        self.image = pygame.image.load(self.img_path).convert()
        self.image.set_colorkey((0, 0, 0))
        self.size = size
        self.image = pygame.transform.scale(self.image, (self.size))
        self.appearing = True
        self.lives = lives
        
        self.piece_size = piece_size
        self.piece_color = piece_color

        self.step = self.piece_size[0]
        self.INC = 2
        
        # position coordinates
        self.x = pos[0]
        self.y = pos[1]
        self.rect = pygame.rect.Rect(self.x, self.y, self.size[0], self.size[1])

        # step of a motorcycle
        self.x_step = 0
        self.y_step = 0

        # at the beginning, each TMoto is not powered by any of the TronFoods
        self.powered = [False, False]

        # holds the pieces of the trail
        self.trail = []
        self.length = length
        self.starting_lenght = length

        # creating a list with images for the explosions
        self.explo_paths = ['src/images/explosion/explo0.png', 'src/images/explosion/explo1.png', 'src/images/explosion/explo2.png']
        self.explosion = []
        
        for path in self.explo_paths:
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (60, 60))
            self.explosion.append(image)
        
        pygame.display.update()
    #

    def explode(self):
        """ WRITE HERE THE DOCS FOR THIS FUNCTION!!! """
        for status in self.explosion:
            self.surface.blit(status, (self.x, self.y))
            pygame.display.update()
            pygame.time.wait(5)
    #

    def set_direction(self, direction):
        """ WRITE HERE THE DOCS FOR THIS FUNCTION!!! """
        self.direction = direction
    #

    def set_position(self, step):
        """ WRITE HERE THE DOCS FOR THIS FUNCTION!!! """
        self.x_step = step[0]
        self.y_step = step[1]
    #

    def collides(self, rect):
        """ WRITE HERE THE DOCS FOR THIS FUNCTION!!! """
        if self.rect.colliderect(rect):
            return True
        else:
            return False
    #
    
    def colliding(self, moto):
        """ WRITE HERE THE DOCS FOR THIS FUNCTION!!! """
        for x in moto.trail[0:-1]:
            if self.collides(x):
                return TMoto.STATUS[1]
        if self.collides(moto.rect):
            return TMoto.STATUS[2]
        return TMoto.STATUS[0]
    #

    def crashing(self, moto):
        """This method returns 3 possible values:
        0 = 'self' does NOT collide with 'moto';
        1 = 'self' collides with 'moto';
        2 = 'self' and 'moto' collide both;
        The method calls colliding (which calls 'collides') to verify it there's a collision
        The method is also responsible for calling 'explode' and reduce 'lives', if a collision occurs.
        """
        # YES
        if self.colliding(moto) == TMoto.STATUS[1]:
            self.explosion_sound.play(0)
            self.explode()
            self.lives -= 1
            self.appearing = False
            return TMoto.STATUS[1]
        # BOTH
        elif self.colliding(moto) == TMoto.STATUS[2]:
            self.explosion_sound.play(0)
            # explode both and decrease life points of 'self' and 'moto'
            self.explode()
            moto.explode()
            self.lives -= 1
            moto.lives -= 1
            self.appearing = False
            moto.appearing = False
            return TMoto.STATUS[2]
        # NO
        else: 
            return TMoto.STATUS[0]
    #           

    def update_rect(self):
        """ WRITE HERE THE DOCS FOR THIS FUNCTION!!! """
        self.rect = pygame.rect.Rect(self.x-12, self.y-12, self.size[0], self.size[1])
    #

    def update_pos(self):
        """managing when you go through the walls"""
        self.pass_through_walls()
        self.x += self.x_step
        self.y += self.y_step
        self.update_rect()
    #
    
    def stop(self):
        """ WRITE HERE THE DOCS FOR THIS FUNCTION!!! """
        self.x_step = self.y_step = 0
    #

    def update_trail(self):
        '''Updates the trail of the TMoto'''
        self.trail.append(pygame.rect.Rect(self.x, self.y, self.piece_size[0], self.piece_size[1]))
        while len(self.trail) > self.length:
            del self.trail[0]
    #

    def pass_through_walls(self):
        """ WRITE HERE THE DOCS FOR THIS FUNCTION!!! """
        if self.x >= self.surface.get_rect()[2]:
            self.x = 0
        if self.x < 0:
            self.x = self.surface.get_rect()[2]
        if self.y >= self.surface.get_rect()[3]:
            self.y = 0
        if self.y < 0:
            self.y = self.surface.get_rect()[3]
    #

    def proceed(self):
        """This function seems stupid..."""
        self.set_direction(self.direction)
        if self.direction == "right":
            self.set_position((self.step, 0))
        if self.direction == "left":
            self.set_position((-self.step, 0))
        if self.direction == "up":
            self.set_position((0, -self.step))
        if self.direction == "down":
            self.set_position((0, self.step))
    #
     
    def get_power_from(self, obj):
        """ WRITE HERE THE DOCS FOR THIS FUNCTION!!! """
        # We want to establish normal 'self.step' or 'self.length',
        # iff the timer has already finished.
        if self.timer.ringing():
            # If SPEED power is active and 'obj' is of that type of power
            if self.powered[0]: 
                self.step -= self.INC
                self.length = self.starting_lenght
                self.powered[0] = False
                self.powered[1] = False
                self.timer.stop()

            # If SIZE power is active and 'obj' is of that type of power                
            elif self.powered[1]:                
                self.length = self.starting_lenght
                self.powered[1] = False
                self.powered[0] = False
                self.timer.stop()
                self.update_trail()
                self.timer.stop()
                
            self.proceed()

        # If self is colliding 'obj'
        if self.collides(obj):
            if obj.power == TFood.powers[0] and not self.powered[0]:
                self.powered[0] = True
                self.step += self.INC
                self.timer.start()
            if obj.power == TFood.powers[0] and self.powered[0]:
                self.timer.stop()
                self.timer.start()
            elif obj.power == TFood.powers[1] and not self.powered[1]:
                self.powered[1] = True
                self.length = round(self.length * 2)
                self.update_trail()
                self.timer.start()
            if obj.power == TFood.powers[1] and self.powered[1]:
                self.timer.stop()
                self.timer.start()
                       
            self.proceed()
                    
            # a new 'obj' is generated, iff it was used
            obj.generate()
            obj.appear()

        self.timer.inc() # increments timer, iff it has already started           
    #
            
    def move(self):
        """Changes the directions of the TMoto"""
        self.update_trail()
        
        if self.direction == 'right':
            if self.previous_direction == 'left':
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.previous_direction == 'up':
                self.image = pygame.transform.rotate(self.image, 270)
            elif self.previous_direction == 'down':
                self.image = pygame.transform.rotate(self.image, 90)

        elif self.direction == 'left':
            if self.previous_direction == 'right':
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.previous_direction == 'up':
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.previous_direction == 'down':
                self.image = pygame.transform.rotate(self.image, 270)

        elif self.direction == 'up':
            if self.previous_direction == 'left':
                self.image = pygame.transform.rotate(self.image, 270)
            elif self.previous_direction == 'right':
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.previous_direction == 'down':
                self.image = pygame.transform.rotate(self.image, 180)

        elif self.direction == 'down':
            if self.previous_direction == 'left':
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.previous_direction == 'right':
                self.image = pygame.transform.rotate(self.image, 270)
            elif self.previous_direction == 'up':
                self.image = pygame.transform.rotate(self.image, 180)
                
        self.previous_direction = self.direction
        
        # shoget_winnerg the head of the Motorcycle
        self.surface.blit(self.image, (self.trail[-1][0]-12, self.trail[-1][1]-12))

        # displays the trail
        for x in self.trail[:-1]: # getting elements from start to end - 1
            self.surface.fill(self.piece_color, x)
    #
    
# end TMoto
