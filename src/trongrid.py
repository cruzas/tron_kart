"""
This file should contain just the main class of the game: TronGrid
Other classes should be found in other files
"""

# STANDARD
import random
import sys

# DO NOT CHANGE THE ORDER OF THE IMPORTS!!!
from src.tutilities import get_file_names
from src.tcolors import *
from src.tmoto import * # imports TMoto, TTimer, TFood and pygame
from src.tboard import TBoard
from src.twindow import TWindow, tkinter


class TronGrid:
    """Main class of the game. It creates the TMoto, TFood and TBoard objects, and manage all the connections."""

    SCORE_SIDES = ["LEFT", "RIGHT"]

    def __init__(self, title='Tron Kart'):
        """Constructor of the main class"""
        if type(title) != str:
            raise TypeError('title is not a str')

        pygame.init()
        pygame.mixer.init()

        self.timer = TTimer(200)

        self.title = title
        self.clock = pygame.time.Clock()

        # REMEMBER TO REFER TO THIS MODULE (src) IN THE PATHS!!!
        self.board = TBoard((800, 450), WHITE, 'src/images/boards/board1.jpg', self.title)
        self.FPS = 60

        # PLAYERS: TO MAKE THE PLAYER SELECT THE IMAGE MAKE A VARIABLE WICH TAKES A NUMBER
        # FROM 0 TO THE NUMBER OF IMAGES-1 AND PUT IT IN SELF_PLAYERS_CHOICE INSTEAD OF THE RANDOM
        self.players_list = get_file_names('src/images/players/', '.png')
        self.players_choice = random.randint(0, len(self.players_list)-1)
        self.img_path = 'src/images/players/' + self.players_list[self.players_choice]
        self.players_list.pop(self.players_choice)
        self.players_choice = random.randint(0, len(self.players_list)-1)
        self.img_path2 = 'src/images/players/' + self.players_list[self.players_choice]

        # THIS VARIABLE IS NOT USED YET
        self.piece_img = 'src/images/trails_pieces/blue.png'

        # FIRST PLAYER SETUP
        self.moto_size = (28, 28)
        self.pos = (100, self.board.resolution[1]/2)
        self.moto = TMoto(self.board.surface, "Kill Bill (S. Jobs)", TMoto.MAX_LIVES, self.img_path, self.pos, TRON_Y, self.piece_img)

        # SECOND PLAYER SETUP
        self.pos_2 = (self.board.resolution[0] - 100, self.board.resolution[1]/2)
        self.moto2 = TMoto(self.board.surface, "Bill Logical Gate", TMoto.MAX_LIVES, self.img_path2, self.pos_2, TRON_O, self.piece_img)

        # POWER
        self.food_img_1 = 'src/images/powerups/speed_up.png'
        self.food_img_2 = 'src/images/powerups/tail_inc.png'

        self.apple = TFood(self.board.surface, self.food_img_1, TFood.powers[0])
        self.kiwi = TFood(self.board.surface, self.food_img_2, TFood.powers[1])

        # SOUNDS: TO MAKE THE PLAYER SELECT THE MUSIC MAKE A VARIABLE WICH TAKES A NUMBER
        # FROM 0 TO THE NUMBER OF SONGS-1 AND PUT IT IN SELF_MUSIC_CHOICE INSTEAD OF THE RANDOM
        self.music_list = get_file_names('src/sounds/background/', '.aiff')
        self.music_choice = random.randint(0,len(self.music_list)-1) #numbers from 0 to number of music files-1
        self.music = 'src/sounds/background/' + self.music_list[self.music_choice]
        self.explosion_sound = pygame.mixer.Sound('src/sounds/explosion.aiff')
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
        """ WRITE HERE THE DOCS FOR THIS FUNCTION!!! """
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
        """ WRITE HERE THE DOCS FOR THIS FUNCTION!!! """
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
        """ WRITE HERE THE DOCS FOR THIS FUNCTION!!! """
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


class Runner():
    """Class used just to create objects that create instances of the game."""
    def __init__(self):
        root = tkinter.Tk()
        twin = TWindow(root, 'Tron Kart')
        root.mainloop()

        if TWindow.proceed:
            tgrid = TronGrid()
    #
#
