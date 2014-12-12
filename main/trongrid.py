"""
This file should contain just the main class of the game: TronGrid
Other classes should be found in other files
"""

from colors import *
import pygame
import random
from get_file_names import get_file_names
import sys
import eztext

#            

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
    #
    
    def start(self):
        self.stop()
        self.started = True
        
    #
    
    def inc(self):
        if self.started:
            if self.t >= self.max:
                self.finished = True
            else:
                self.t += 1

    def ringing(self):
        return self.finished
    #
    
    def stop(self):
        self.started = False ### Is this (-) a mistake? Yes it was
        self.finished = False
        self.t = 0
    #
    
# end TronTimer


class TMoto:
    """Main class containing the TMoto for this game."""

    # static variable
    
    STATUS = [0, 1, 2] # collision status: 0=NO, 1=YES, 2=BOTH
    MAX_LIVES = 3
    

    def __init__(self, surface, name, lives, img_path, pos, piece_color, piece_image, size=(30, 30), piece_size=(4, 4), direction='', length=60):
        self.timer = TronTimer(100) # 100 is the amount of "time" that has to pass
        self.explosion_sound = pygame.mixer.Sound('sounds/explosion.aiff')

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
    
        self.piece_image = piece_image
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
        self.explo_paths = ['images/explosion/explo0.png', 'images/explosion/explo1.png', 'images/explosion/explo2.png']
        self.explosion = []
        
        for path in self.explo_paths:
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (60, 60))
            self.explosion.append(image)
        
        pygame.display.update()
    #

    def explode(self):
        for status in self.explosion:
            self.surface.blit(status, (self.x, self.y))
            pygame.display.update()
            pygame.time.wait(5)
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
        '''Updates the trail of the TMoto'''
        self.trail.append(pygame.rect.Rect(self.x, self.y, self.piece_size[0], self.piece_size[1]))
        while len(self.trail) > self.length:
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
        '''Changes the directions of the TMoto'''
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
    

class TBoard:
    """This class represents the board of a TronGrid object."""
    
    def __init__(self, resolution, color, image_path, title='TBoard'):
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

    def get_middle_coords(self, msg, font_size, bold=False, italic=False):
        """Returns the coordinates to put a centered message to the screen"""
        font = pygame.font.SysFont(None, font_size, bold, italic)
        text = font.render(msg, True, (0, 0, 0))
        rect = text.get_rect()
        return (self.width/2 - rect[2]/2, self.width/2 - rect[3]/2)
    #

    def get_score_coords(self, msg, font_size, side="RIGHT", board_distance=10, bold=False, italic=False):
        font = pygame.font.SysFont(None, font_size, bold, italic)
        text = font.render(msg, True, (0, 0, 0))
        rect = text.get_rect()
        if side == "RIGHT":
            return (self.width - board_distance - rect[2], board_distance)
        elif side == "LEFT": # quite useless
            return (board_distance, board_distance)
    #
        
    
    def write(self, msg, color, font_size, pos='CENTER', bold=False, italic=False):
        """This function writes some text in a surface passed as parameter."""
        font = pygame.font.SysFont(None, font_size, bold, italic)
        text = font.render(msg, True, color)
        
        if pos == 'CENTER':
            rect = text.get_rect()
            x = self.width/2 - rect[2]/2
            y = self.height/2 - rect[3]/2
            self.surface.blit(text, [x, y])
        else:
            self.surface.blit(text, pos)
    #
    
# end TBoard


class TFood:
    """Simple class to represent object of type TFood"""

    # static variable that keeps track of the type of powers-up that a TFood can give
    powers = ["SPEED", "SIZE"]
    
    def __init__(self, surface, img_path, power, size=(30, 30), name=''):

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
    
# end TFood


class TronGrid:
    """Main class of the game. It creates the TMoto, TFood and TBoard objects, and manage all the connections."""

    SCORE_SIDES = ["LEFT", "RIGHT"]

    def __init__(self, title='Tron Grid'):
        """Constructor of the main class"""
        if type(title) != str:
            raise TypeError('title is not a str')
        
        pygame.init()
        pygame.mixer.init()

        self.timer = TronTimer(100)

        self.title = title
        self.clock = pygame.time.Clock()
        
        self.board = TBoard((800, 450), WHITE, 'images/board2.jpg', self.title)
        self.FPS = 60

        # PLAYERS
        self.img_path = 'images/tron.png'
        self.img_path2 = 'images/tron2.png'

        self.piece_img = 'images/blue.png'
        # first player
        
        self.moto_size = (28, 28)
        self.pos = (100, self.board.resolution[1]/2)
        self.moto = TMoto(self.board.surface, "Kill Bill (S. Jobs)", TMoto.MAX_LIVES, self.img_path, self.pos, TRON_Y, self.piece_img)

        # second player
        self.pos_2 = (self.board.resolution[0] - 100, self.board.resolution[1]/2)
        self.moto2 = TMoto(self.board.surface, "Bill Logical Gate", TMoto.MAX_LIVES, self.img_path2, self.pos_2, TRON_O, self.piece_img)

        # POWER
        self.food_img_1 = 'images/random.png'
        self.food_img_2 = 'images/random2.png'

        self.apple = TFood(self.board.surface, self.food_img_1, TFood.powers[0])
        self.kiwi = TFood(self.board.surface, self.food_img_2, TFood.powers[1])

        # SOUNDS TO MAKE THE PLAYER SELECT THE MUSIC MAKE A VARIABLE WICH TAKES A NUMBER
        # FROM 0 TO THE NUMBER OF SONGS-1 AND PUT IT IN SELF_CHOICE INSTEAD OF THE RANDOM
        self.music_list = get_file_names('sounds/background/', '.aiff')
        self.choice = random.randint(0,1) #numbers from 0 to number of music files-1
        self.music = 'sounds/background/' + self.music_list[self.choice]
        self.explosion_sound = pygame.mixer.Sound('sounds/explosion.aiff')
        self.game_music = pygame.mixer.Sound(self.music)
        
        pygame.display.update()
        self.run()
        pygame.quit()
    #
    
    def reset(self):
        """Reset the background and the position of the 2 motos."""
        self.board.update()
        self.moto = TMoto(self.board.surface, self.moto.name, self.moto.lives, self.img_path, self.pos, TRON_Y, self.moto.piece_image)
        self.moto2 = TMoto(self.board.surface, self.moto2.name, self.moto2.lives, self.img_path2, self.pos_2, TRON_O, self.moto2.piece_image)
    #

    def restart(self, name='Mr. Weed', name2='Bush, The Laden'):
        self.board.update()
        self.moto = TMoto(self.board.surface, name, TMoto.MAX_LIVES, self.img_path, self.pos, TRON_Y, self.moto.piece_image)
        self.moto2 = TMoto(self.board.surface, name2, TMoto.MAX_LIVES, self.img_path2, self.pos_2, TRON_O, self.moto2.piece_image)
    #

    def pause(self):
        """Called when the game is paused"""
        paused = True
        msg = "Paused"
        size = 60
        pos = self.board.get_middle_coords(msg, size)
        self.board.write(msg, WHITE, size, (pos[0], pos[1] - 240))

        msg = "Press C to proceed or Q to quit"
        size = 25
        pos = self.board.get_middle_coords(msg, size)
        self.board.write(msg, WHITE, size, (pos[0], pos[1] - 50))

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
            msg = 'Draw!'

        size = 30
        pos = self.board.get_middle_coords(msg, size)
        self.reset()
        self.board.write(msg, WHITE, size)
        
        pygame.display.update()        
        pygame.time.wait(1000)
        
    #
    
    def gameover(self, winner):
        """Game is over. You can start again or quit"""
        game_over = True

        msg = ''
        size = 40

        if winner is None:
            msg = "That's tie!"
        else:
            msg = "Congratulations " + winner.name + ", you won!"

        pos = self.board.get_middle_coords(msg, size)
        self.board.write(msg, WHITE, size, (pos[0], pos[1] - 240))

        msg = "Press C to play again or Q to quit"
        size = 25
        pos = self.board.get_middle_coords(msg, size)
        self.board.write(msg, WHITE, size, (pos[0], pos[1]-50))
        
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
                        self.game_music.stop()
                        self.run()
    #
    
    def set_score(self, score, player, pos="RIGHT"):
        """Changes the set_score of the players"""
        msg = player + ": " + str(score)
        font_size = 30
        if pos == TronGrid.SCORE_SIDES[0] or pos == TronGrid.SCORE_SIDES[1]:
            pos = self.board.get_score_coords(msg, font_size, pos)            
            self.board.write(msg, WHITE, font_size, pos)
    #

    def check_winner(self):
        """If there's a winner it will be passed to the self.gameover method."""
        if self.moto.lives <= 0 and self.moto2.lives <= 0:
            self.gameover(None)
        if self.moto.lives <= 0:
            self.gameover(self.moto2) 
        if self.moto2.lives <= 0:
            self.gameover(self.moto)
    #

    def winner(self):
        if self.moto.lives == 0 or self.moto2.lives == 0:
            return True
        return False
    #
    
    def run(self):
        """Main function of the whole game, specifically of the TronGrid class."""
        running = True
        
        # generates and shows first power up objects
        self.apple.generate()
        self.apple.appear()
        self.kiwi.generate()
        self.kiwi.appear()

        self.game_music.play(-1)
        
        while running:
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.KEYDOWN:
                    self.moto.previous_direction = self.moto.direction
                    self.moto2.previous_direction = self.moto2.direction

                     # FIRST PLAYER (MOVEMENT)
                    if event.key == pygame.K_a and self.moto.previous_direction != 'right':
                        self.moto.set_direction('left')
                        self.movement = 'left'
                        self.moto.set_position((-self.moto.step, 0))
                        
                    elif event.key == pygame.K_d and self.moto.previous_direction != 'left':
                        self.moto.set_direction('right')
                        self.movement = 'right'
                        self.moto.set_position((self.moto.step, 0))
                        
                    elif event.key == pygame.K_w and self.moto.previous_direction != 'down':
                        self.moto.set_direction('up')
                        self.movement = 'up'
                        self.moto.set_position((0, -self.moto.step))
                    
                    elif event.key == pygame.K_s and self.moto.previous_direction != 'up':
                        self.moto.set_direction('down')
                        self.movement = 'down'
                        self.moto.set_position((0, self.moto.step))
                    elif event.key == pygame.K_e:
                        self.moto.stop()

                    # SECOND PLAYER (MOVEMENT)
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
                    elif event.key == pygame.K_RSHIFT:
                        self.moto2.stop()
            
                    # pause
                    if event.key == pygame.K_p:
                        self.pause()
 
            # end for

            # update positions of TMotos according to the new direction + 'step'
            self.moto.update_pos()
            self.moto2.update_pos()
            self.board.update()

            # check collisions and if there's a winner
            if self.moto.crashing(self.moto2) != TMoto.STATUS[0] and not self.winner():
                self.show_status()
            elif self.moto2.crashing(self.moto) != TMoto.STATUS[0] and not self.winner():
                self.show_status()
            else:
                self.check_winner()
                        
            self.moto.move()
            self.moto2.move()
            
            self.apple.appear()
            self.kiwi.appear()
            
            # setting the set_score of the 2 players
            self.set_score(self.moto.lives, self.moto.name, TronGrid.SCORE_SIDES[0])
            self.set_score(self.moto2.lives, self.moto2.name)

            # checking if self.moto is hitting some power
            self.moto.get_power_from(self.apple)
            self.moto.get_power_from(self.kiwi)

            # checking if self.moto2 is doing the same thing
            self.moto2.get_power_from(self.apple)
            self.moto2.get_power_from(self.kiwi)
            
            # setting the clock frame rate and updating the display
            self.clock.tick(self.FPS)
            pygame.display.update()
    #

    
# end TronGrid

tron_grid = TronGrid() # TronGrid object := starts all the game

