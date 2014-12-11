"""
This file should contain just the main class of the game: TronGrid
Other classes should be found in other files
"""

from colors import *
import pygame
import random


class TronTimer:
    """This class should only be used for this project.
    It simulates a Timer that has to be used inside a while or for loop.
    The class uses a counter variable as time counter."""
    def __init__(self, MAX):
        """MAX represents the TronTimer 'time' that a TronTimer object has to 'wait'."""
        self.max = MAX
        self.t = 0
        self.started = False
        self.finished = False

    def start(self):
        self.stop()
        self.started = True
        
    def inc(self):
        if self.started:
            if self.t >= self.max:
                self.finished = True
            else:
                self.t += 1

    def stopped(self):
        return self.finished

    def stop(self):
        self.started - False
        self.finished = False
        self.t = 0
    #
    
# end TronTimer


class TronMoto:
    """Main class containing the TronMoto for this game."""

    # static variable
    BOTH = 2 # when 2 motorcycles hit each other by the head
    LIVES = 3

    def __init__(self, surface, name, lives, img_path, pos, piece_color, size=(30, 30), piece_size=(4, 4), direction='', length=60):

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
        
        self.timer = TronTimer(100) # 100 is the amount of "time" that has to pass
        
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

        self.accelerating = False

        # holds the pieces of the trail
        self.trail = []
        self.length = length

        # creating a list with images for the explosions
        self.explo_paths = ['images/explosion/explo0.png', 'images/explosion/explo1.png', 'images/explosion/explo2.png']
        self.explosion = []
        
        for path in self.explo_paths:
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (60, 60))
            self.explosion.append(image)
            
        self.lives = lives
        
        pygame.display.update()
    #

    def explode(self):
        for status in self.explosion:
            self.surface.blit(status, (self.x, self.y))
            pygame.display.update()
            pygame.time.wait(5)
    #

    def decrease_trail(self, amount):
        if len(self.trail) > amount:
            n = 0
            while n < amount:
                del self.trail[0]
                n += 1
    #

    def set_direction(self, direction):
        self.direction = direction
    #

    def set_position(self, step):
        self.x_step = step[0]
        self.y_step = step[1]
    #

    def collides(self, rect):
        if self.rect.colliderect(rect):
            return True
        else:
            return False
    #
    
    def colliding(self, moto):
        for x in moto.trail[0:-1]:
            if self.collides(x):
                return True
        if self.collides(moto.rect):
            return TronMoto.BOTH
        return False
    #

    def update_rect(self):
        self.rect = pygame.rect.Rect(self.x-12, self.y-12, self.size[0], self.size[1])
    #

    def update_pos(self):
         # managing when you go through the walls
        self.pass_through_walls()
        self.x += self.x_step
        self.y += self.y_step
        self.update_rect()
    #
    
    def stop(self):
        self.x_step = self.y_step = 0
    #

    def update_trail(self):
        '''Updates the trail of the TronMoto'''
        self.trail.append(pygame.rect.Rect(self.x, self.y, self.piece_size[0], self.piece_size[1]))
        if len(self.trail) > self.length:
            del self.trail[0]
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

    def get_power(self, obj):
        
        if self.accelerating and self.timer.stopped():
            self.step -= self.INC
            self.accelerating = False
            self.timer.stop()

            self.set_direction(self.direction)
            if self.direction == "right":
                self.set_position((self.step, 0))
            if self.direction == "left":
                self.set_position((-self.step, 0))
            if self.direction == "up":
                self.set_position((0, -self.step))
            if self.direction == "down":
                self.set_position((0, self.step))       

        if self.collides(obj):
            if not self.accelerating:
                self.step += self.INC
                self.accelerating = True
                self.timer.start()

                self.decrease_trail(self.length / 2)
                
                self.set_direction(self.direction)

                if self.direction == "right":
                    self.set_position((self.step, 0))
                if self.direction == "left":
                    self.set_position((-self.step, 0))
                if self.direction == "up":
                    self.set_position((0, -self.step))
                if self.direction == "down":
                    self.set_position((0, self.step))

            # generates and makes appear an new obj
            obj.generate()
            obj.appear()

        self.timer.inc() # increments timer if it has started           
    #
            
    
    def move(self):
        '''Changes the directions of the TronMoto'''
        self.update_trail()
        
        if self.direction == 'right':
            if self.previous_direction == 'left':
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.previous_direction == 'right':
                self.image = pygame.transform.rotate(self.image, 0)
            elif self.previous_direction == 'up':
                self.image = pygame.transform.rotate(self.image, 270)
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
                self.image = pygame.transform.rotate(self.image, 270)

        elif self.direction == 'up':
            if self.previous_direction == 'left':
                self.image = pygame.transform.rotate(self.image, 270)
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
                self.image = pygame.transform.rotate(self.image, 270)
            elif self.previous_direction == 'up':
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.previous_direction == 'down':
                self.image = pygame.transform.rotate(self.image, 0)
                
        self.previous_direction = self.direction
        
        # showing the head of the Motorcycle
        self.surface.blit(self.image, (self.trail[-1][0]-12, self.trail[-1][1]-12))

        # displays the trail
        for x in self.trail[:-1]: # getting elements from start to end - 1
            self.surface.fill(self.piece_color, x)
    #
    
# end TronMoto
    

class TronBoard:
    """This class represents the board of a TronGrid object."""
    
    def __init__(self, resolution, color, image_path, title='TronBoard'):
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

        # in case the image of the background is not loaded
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

    def get_middle_coords(self, msg, size, color=WHITE, bold=False, italic=False):
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
    
# end TronBoard


class TronFood:
    """Simple class to represent object of type TronFood"""

    # static variable that keeps track of the type of powers-up that a TronFood can give
    powers = ["SPEED", "SIZE"]
    
    def __init__(self, surface, img_path, power, size=(30, 30), name=''):

        if power not in TronFood.powers:
            raise ValueError('power has not a correct value')
        
        self.name = name
        self.power = power # setting the type of power
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
    """Main class of the game. It creates the TronMoto, TronFood and TronBoard objects, and manage all the connections."""
    
    def __init__(self, title='Tron Grid'):
        """Constructor of the main class"""
        if type(title) != str:
            raise TypeError('title is not a str')
        
        pygame.init()
        pygame.mixer.init()
        
        self.title = title
        self.clock = pygame.time.Clock()
        self.board = TronBoard((800, 600), WHITE, 'images/board2.jpg', self.title)
        self.FPS = 60

        # PLAYERS
        self.img_path = 'images/tron.png'

        # first player
        self.moto_size = (28, 28)
        self.pos = (100, self.board.resolution[1]/2)
        self.moto = TronMoto(self.board.surface, "Steven Work", TronMoto.LIVES, self.img_path, self.pos, piece_color=TRON_Y)

        # second player
        self.pos_2 = (self.board.resolution[0] - 100, self.board.resolution[1]/2)
        self.moto2 = TronMoto(self.board.surface, "Bill Logical Gate", TronMoto.LIVES, self.img_path, self.pos_2, piece_color=TRON_O)
        
        # POWER
        self.food_img_1 = 'images/random.png'
        self.food_img_2 = 'images/random.png'

        self.apple = TronFood(self.board.surface, self.food_img_1, TronFood.powers[0])
        self.kiwi = TronFood(self.board.surface, self.food_img_2, TronFood.powers[1])

        pygame.display.update()
        self.run()
        pygame.quit()
    #
    
    def reset(self):
        """Reset the background and the position of the 2 motos."""
        self.board.update()
        self.moto = TronMoto(self.board.surface, self.moto.name, self.moto.lives, self.img_path, self.pos, piece_color=TRON_Y)
        self.moto2 = TronMoto(self.board.surface, self.moto2.name, self.moto2.lives, self.img_path, self.pos_2, piece_color=TRON_O)
    #

    def restart(self, name='PLAYER 1', name2='PLAYER 2'):
        self.board.update()
        self.moto = TronMoto(self.board.surface, name, TronMoto.LIVES, self.img_path, self.pos, piece_color=TRON_Y)
        self.moto2 = TronMoto(self.board.surface, name2, TronMoto.LIVES, self.img_path, self.pos_2, piece_color=TRON_O)
        

    def pause(self):
        """Called when the game is paused"""
        paused = True
        msg = "Paused"
        size = 60
        pos = self.board.get_middle_coords(msg, size)
        self.board.write(msg, WHITE, (pos[0], pos[1] - 110), size)

        msg = "Press C to continue or Q to quit"
        size = 25
        pos = self.board.get_middle_coords(msg, size)
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

    def manage_collisions(self):
        """Check if the 2 TronMoto are colliding. 
        If yes, the one that hit the other disappears."""
        
        # Checks if the self.moto is colliding with the other TronMoto
        if self.moto2.appearing:
            if self.moto.colliding(self.moto2) == True:
                self.explosion_sound.play(0)
                self.moto.explode()
                self.moto.lives -= 1
                self.moto.appearing = False

                self.win()
                self.moto2.move()
                self.show_status()
                
            elif self.moto.appearing:
                self.moto.move()
        else:
            self.moto.move()

        # Checks if the self.moto2 is colliding with the other TronMoto
        if self.moto.appearing:
            # moto2 will be "destroyed"
            if self.moto2.colliding(self.moto) == True:
                self.explosion_sound.play(0)
                self.moto2.explode()
                self.moto2.lives -= 1
                self.moto2.appearing = False
                
                self.win()
                self.moto.move()
                self.show_status()
                
            elif self.moto2.appearing:
                self.moto2.move()
        else:
            self.moto2.move()
    #

    def show_status(self):
        winning_player = ''
        msg = ''
        
        if self.moto.lives != self.moto2.lives:
            if self.moto.lives > self.moto2.lives:
                winning_player = self.moto.name
            elif self.moto2.lives > self.moto.lives:
                winning_player = self.moto2.name
            msg = winning_player + " is winning!"
        else:
            msg = 'Nobody is winning!'

        size = 30
        pos = self.board.get_middle_coords(msg, size)

        self.reset()
        
        self.board.write(msg, WHITE)
        pygame.display.update()
        
        pygame.time.wait(1000)

    #
    
    def gameover(self, winner):
        """Game is over. You can start again or quit"""
        game_over = True

        msg = "Congratulations " + winner.name + ", you won!"
        size = 40
        pos = self.board.get_middle_coords(msg, size)
        self.board.write(msg, WHITE, (pos[0], pos[1] - 110), size)


        msg = "Press C to play again or Q to quit"
        size = 25
        pos = self.board.get_middle_coords(msg, size)
        self.board.write(msg, WHITE, (pos[0], pos[1]), size)
        
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
                        self.restart()
                        
                        game_over == False
                        self.run()
    #
    
    def set_score(self, score, player, pos=(10, 10)):
        """Changes the set_score of the players"""
        self.board.write(player + ': ' + str(score), WHITE, pos)
    #

    def win(self):
        """If there's a winner, it will be passed to the self.gameover method."""
        if self.moto.lives == 0:
            self.gameover(self.moto2) 
        if self.moto2.lives == 0:
            self.gameover(self.moto)

    def run(self):
        """Main function of the whole game, specifically of the TronGrid class."""
        running = True
        
        # generates and shows first power up objects
        self.apple.generate()
        self.apple.appear()
        self.kiwi.generate()
        self.kiwi.appear()

        self.explosion_sound = pygame.mixer.Sound('sounds/explosion.aiff')
        ## self.game_music = pygame.mixer.Sound('backgroun_music_path')

        ## self.game_music.play(-1)
        while running:

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.KEYDOWN:
                    self.moto.previous_direction = self.moto.direction
                    self.moto2.previous_direction = self.moto2.direction

                    # managing the first moto movement
                    if event.key == pygame.K_a and self.moto.previous_direction != 'right':
                        self.moto.set_direction('left')
                        self.moto.set_position((-self.moto.step, 0))
                        
                    elif event.key == pygame.K_d and self.moto.previous_direction != 'left':
                        self.moto.set_direction('right')
                        self.moto.set_position((self.moto.step, 0))
                        
                    elif event.key == pygame.K_w and self.moto.previous_direction != 'down':
                        self.moto.set_direction('up')
                        self.moto.set_position((0, -self.moto.step))
                    
                    elif event.key == pygame.K_s and self.moto.previous_direction != 'up':
                        self.moto.set_direction('down')
                        self.moto.set_position((0, self.moto.step))

                    # managing the second moto movement
                    if event.key == pygame.K_LEFT and self.moto2.previous_direction != 'right':
                        self.moto2.set_direction('left')
                        self.moto2.set_position((-self.moto2.step, 0))
                        
                    elif event.key == pygame.K_RIGHT and self.moto2.previous_direction != 'left':
                        self.moto2.set_direction('right')
                        self.moto2.set_position((self.moto2.step, 0))
                        
                    elif event.key == pygame.K_UP and self.moto2.previous_direction != 'down':
                        self.moto2.set_direction('up')
                        self.moto2.set_position((0, -self.moto2.step))
                        
                    elif event.key == pygame.K_DOWN and self.moto2.previous_direction != 'up':
                        self.moto2.set_direction('down')
                        self.moto2.set_position((0, self.moto2.step))

                    # pause
                    if event.key == pygame.K_p:
                        self.pause()
 
            # end for
            
            # moving the moto
            self.moto.update_pos()
            self.moto2.update_pos()

            # updating the board: color and image
            self.board.update() 

            self.manage_collisions()

            # make another apple appears
            self.apple.appear()
            self.kiwi.appear()
            
            # setting the set_score of the 2 players
            self.set_score(self.moto.lives, 'P1')
            self.set_score(self.moto2.lives, 'P2', pos=(self.board.width - 72, 10))

            # checking if self.moto is hitting some power
            self.moto.get_power(self.apple)
            self.moto.get_power(self.kiwi)

            # checking if self.moto2 is doing the same thing
            self.moto2.get_power(self.apple)
            self.moto2.get_power(self.kiwi)
            
            # setting the clock frame rate and updating the display
            self.clock.tick(self.FPS)
            pygame.display.update()
    #
    
# end TronGrid

tron_grid = TronGrid() # TronGrid object := starts all the game
