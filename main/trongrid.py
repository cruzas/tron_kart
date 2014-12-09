"""
This file should contain just the main class of the game: TronGrid
Other classes should be found in other files
"""

from colors import *
import pygame
import random


class Moto:

    # static variable
    BOTH = 2 # when 2 motorcycles hit each other by the head
    
    def __init__(self, surface, img_path, pos, piece_color, size=(28, 28), piece_size=(4, 4), direction='', length=80):
        
        self.surface = surface
        self.direction = direction
        self.previous_direction = self.direction
        self.img_path = img_path
        self.image = pygame.image.load(self.img_path).convert()
        self.image.set_colorkey((0, 0, 0))
        self.size = size
        self.image = pygame.transform.scale(self.image, (self.size))
        self.isappearing = True

        self.piece_size = piece_size
        self.piece_color = piece_color
        
        self.step = self.piece_size[0]
        self.acceleration = 0

        # position coordinates
        self.x = pos[0]
        self.y = pos[1]
        self.rect = pygame.rect.Rect(self.x, self.y, self.size[0], self.size[1])

        # speed of a moto
        self.x_speed = 0
        self.y_speed = 0

        # holds the pieces of the trail
        self.buffer = []
        self.length = length 

        self.life_points = 100
        pygame.display.update()
    #

    def set_direction(self, direction):
        self.direction = direction
    #

    def set_speed(self, speed):
        self.x_speed = speed[0]
        self.y_speed = speed[1]
    #


    def collides(self, rect):
        if self.rect.colliderect(rect):
            return True
        else:
            return False
    #
    
    def iscolliding(self, moto):
        for x in moto.buffer[0:-1]:
            if self.collides(x):
                return True
        if self.collides(moto.rect):
            return Moto.BOTH
        return False
    #

    def update_rect(self):
        self.rect = pygame.rect.Rect(self.x, self.y, self.size[0], self.size[1])
    #

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.update_rect()
    #
    
    def stop(self):
        self.x_speed = self.y_speed = 0
    #

    def update(self):
        '''Updates the trail of the Moto'''
        self.buffer.append(pygame.rect.Rect(self.x, self.y, self.piece_size[0], self.piece_size[1]))
        if len(self.buffer) > self.length:
            del self.buffer[0]
    #

    def pass_through_walls(self):
        if self.x >= self.surface.get_rect()[2]:
            self.x = 0
        if self.x < 0:
            self.x = self.surface.get_rect()[2]
        if self.y >= self.surface.get_rect()[3]:
            self.y = 0
        if self.y < 0:
            self.y = self.surface.get_rect()[3]
    #
    
    def show(self):
        '''Changes the directions of the Moto'''
        
        if self.direction == 'right':
            if self.previous_direction == 'left':
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.previous_direction == 'right':
                self.image = pygame.transform.rotate(self.image, 0)
            elif self.previous_direction == 'up':
                self.image = pygame.transform.rotate(self.image, -90)
            elif self.previous_direction == 'down':
                self.image = pygame.transform.rotate(self.image, 90)

        elif self.direction == 'left':
            if self.previous_direction == 'left':
                self.image = pygame.transform.rotate(self.image, 0)
            elif self.previous_direction == 'right':
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.previous_direction == 'up':
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.previous_direction == 'down':
                self.image = pygame.transform.rotate(self.image, -90)

        elif self.direction == 'up':
            if self.previous_direction == 'left':
                self.image = pygame.transform.rotate(self.image, -90)
            elif self.previous_direction == 'right':
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.previous_direction == 'up':
                self.image = pygame.transform.rotate(self.image, 0)
            elif self.previous_direction == 'down':
                self.image = pygame.transform.rotate(self.image, 180)

        elif self.direction == 'down':
            if self.previous_direction == 'left':
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.previous_direction == 'right':
                self.image = pygame.transform.rotate(self.image, -90)
            elif self.previous_direction == 'up':
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.previous_direction == 'down':
                self.image = pygame.transform.rotate(self.image, 0)
                
        self.previous_direction = self.direction

        # displays the moto
        self.surface.blit(self.image, (self.buffer[-1][0]-12, self.buffer[-1][1]-12))

        # displays the trail
        for x in self.buffer[:-1]: # getting elements from start to end - 1
            self.surface.fill(self.piece_color, x)
    #
#
    

class Board:
    def __init__(self, resolution, color, image_path, title='Board'):
        self.title = title
        self.resolution = resolution
        self.width = resolution[0]
        self.height = resolution[1]
        self.color = color  # background color
        self.image_path = image_path        
        self.surface = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption(self.title)
        self.surface.fill(self.color)
        self.using_img = True
        try:
            self.image = pygame.image.load(self.image_path).convert()
            self.image = pygame.transform.scale(self.image, self.resolution)
        except (pygame.error, Exception):
            self.using_img = False
    #

    def update(self):
        self.surface.fill(self.color)
        if self.using_img:
            self.surface.blit(self.image, (0, 0))
    #

    def middle_coords(self, msg, size, color=WHITE, bold=False, italic=False):
        """Returns the coordinates to put a centered message to the screen"""
        font = pygame.font.SysFont(None, size, bold, italic)
        text = font.render(msg, True, color)
        rect = text.get_rect()
        return self.width/2 - rect[2]/2, self.width/2 - rect[3]/2
    #
    
    def write(self, msg, color, pos='CENTER', size=30, bold=False, italic=False):
        """This function writes some text in a surface passed as parameter."""
        font = pygame.font.SysFont(None, size, bold, italic)
        text = font.render(msg, True, color)
        
        if pos == 'CENTER':
            rect = text.get_rect()
            x = self.width/2 - rect[2]/2
            y = self.height/2 - rect[3]/2
            self.surface.blit(text, [x, y])
        else:
            self.surface.blit(text, pos)
    #
#


class TronFood:
    """Simple class to represent object of type TronFood"""
    def __init__(self, surface, img_path, size=(30, 30), name='', power=10):
        
        self.name = name
        self.power = power

        # coordinates of the TronFood object in the surface
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
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
    #
    
    def generate(self):
        self.x = round(random.randrange(0, self.surface.get_rect()[2] - self.width))
        self.y = round(random.randrange(0, self.surface.get_rect()[3] - self.height))
        self.update_rect()
    #
    
    def appear(self):
        self.surface.blit(self.image, (self.x, self.y))
    #
    
# end TronFood


class TronGrid:
    def __init__(self, title='Tron Grid'):
        """Constructor of the main class"""
        pygame.init()

        if type(title) != str:
            raise TypeError('title is not a str')

        self.title = title
        self.clock = pygame.time.Clock()
        self.board = Board((640, 480), WHITE, 'images/board2.jpg', self.title)
        self.FPS = 50

        self.img_path = 'images/tron.png'

        # first player
        self.pos = (100, self.board.resolution[1]/2)
        self.moto = Moto(self.board.surface, self.img_path, self.pos, piece_color=TRONB)

        # second player
        self.pos_2 = (self.board.resolution[0] - 100, self.board.resolution[1]/2)
        self.moto_2 = Moto(self.board.surface, self.img_path, self.pos_2, piece_color=TRONO)  
        
        self.food_img_path = 'images/apple.png'
        
        # creating a TronFood to increase power
        self.apple = TronFood(self.board.surface, self.food_img_path)

        pygame.display.update()
        self.run()
        pygame.quit()
    #
    
    def reset(self):
        """Reset the background and the position of the 2 motos."""
        self.board.update()
        self.moto = Moto(self.board.surface, self.img_path, self.pos, piece_color=TRONB)
        self.moto_2 = Moto(self.board.surface, self.img_path, self.pos_2, piece_color=TRONO)  
    #
    
    def pause(self):
        """Called when the game is paused"""
        
        paused = True
        
        msg = "Paused"
        size = 60
        pos = self.board.middle_coords(msg, size)
        self.board.write(msg, WHITE, (pos[0], pos[1] - 110), size)

        msg = "Press C to continue or Q to quit"
        size = 25
        pos = self.board.middle_coords(msg, size)
        self.board.write(msg, WHITE, (pos[0], pos[1]), size)

        pygame.display.update()

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()
            self.clock.tick(5)
    #

    def check_collisions(self):
        """Check if the 2 motos collide; if yes, the one that collided diseappears."""
        if self.moto_2.isappearing:
            if self.moto.iscolliding(self.moto_2) == True:
                self.board.update()
                self.moto_2.show()
                self.moto.isappearing = False
                self.gameover()
                
            elif self.moto.isappearing:
                self.moto.show()
        else:
            self.moto.show()

        if self.moto.isappearing:
            if self.moto_2.iscolliding(self.moto) == True:
                self.moto_2.isappearing = False
                self.board.update()
                self.moto.show()
                self.gameover()
                
            elif self.moto_2.isappearing:
                self.moto_2.show()
        else:
            self.moto_2.show()
    #

    def eating(self):
        """This function is called every loop game to change the speed of the motos,
in case they acquire power (apples)"""
        if self.moto.collides(self.apple):
            if self.moto.step < 6:
                self.moto.acceleration += 2
                self.moto.step += self.moto.acceleration
            else:
                self.moto.step -= self.moto.acceleration
                self.moto.acceleration = 0
                
            self.apple.generate()
            self.apple.appear()

        if self.moto_2.collides(self.apple):
            
            if self.moto_2.step < 6:
                self.moto_2.acceleration += 2
                self.moto_2.step += self.moto_2.acceleration
            else:
                self.moto_2.step -= self.moto_2.acceleration
                self.moto_2.acceleration = 0
                
            self.apple.generate()
            self.apple.appear()
    #
    
    def gameover(self):
        """Game is over. You can start again or quit"""
        game_over = True
        self.board.write("Game over, press C to play again or Q to quit", WHITE)
        pygame.display.update()
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = False
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_c:
                        self.reset()
                        game_over == False
                        self.run()
    #
    
    def score(self, score, pos=(10, 10)):
        """Changes the score of the players"""
        self.board.write('Score: ' + str(score), WHITE, pos)
    #
    
    def run(self):
        """Main function of the whole game, specifically of the TronGrid class."""
        
        running = True
        
        self.apple.generate()
        self.apple.appear()
        
        while running:

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.KEYDOWN:
                    self.moto.previous_direction = self.moto.direction
                    self.moto_2.previous_direction = self.moto_2.direction

                    # managing the first moto movement
                    if event.key == pygame.K_LEFT and self.moto.previous_direction != 'right':
                        self.moto.set_direction('left')
                        self.moto.set_speed((-self.moto.step, 0))
                        
                    elif event.key == pygame.K_RIGHT and self.moto.previous_direction != 'left':
                        self.moto.set_direction('right')
                        self.moto.set_speed((self.moto.step, 0))
                        
                    elif event.key == pygame.K_UP and self.moto.previous_direction != 'down':
                        self.moto.set_direction('up')
                        self.moto.set_speed((0, -self.moto.step))
                        
                    elif event.key == pygame.K_DOWN and self.moto.previous_direction != 'up':
                        self.moto.set_direction('down')
                        self.moto.set_speed((0, self.moto.step))

                    # managing the second moto movement
                    if event.key == pygame.K_a and self.moto_2.previous_direction != 'right':
                        self.moto_2.set_direction('left')
                        self.moto_2.set_speed((-self.moto_2.step, 0))
                        
                    elif event.key == pygame.K_d and self.moto_2.previous_direction != 'left':
                        self.moto_2.set_direction('right')
                        self.moto_2.set_speed((self.moto_2.step, 0))
                        
                    elif event.key == pygame.K_w and self.moto_2.previous_direction != 'down':
                        self.moto_2.set_direction('up')
                        self.moto_2.set_speed((0, -self.moto_2.step))
                        
                    elif event.key == pygame.K_s and self.moto_2.previous_direction != 'up':
                        self.moto_2.set_direction('down')
                        self.moto_2.set_speed((0, self.moto_2.step))

                    # pause
                    if event.key == pygame.K_p:
                        self.pause()
 
            # end for

            # managing when you go through the walls
            self.moto.pass_through_walls()
            self.moto_2.pass_through_walls()
            
            # moving the moto
            self.moto.move()
            self.moto_2.move()

            # updating the board: color and image
            self.board.update() 

            # updating trail of the motorcycles
            self.moto.update()
            self.moto_2.update()

            self.check_collisions()

            # make another apple appears
            self.apple.appear()
                    
            # setting the score of the 2 players
            self.score(self.moto.life_points)
            self.score(self.moto_2.life_points, pos=(self.board.width - 100, 10))

            self.eating() # if you eat an 'apple' your speed increases.
    
            self.clock.tick(self.FPS)
            pygame.display.update()
    #

#

tron_grid = TronGrid() # TronGrid object := starts all the game
