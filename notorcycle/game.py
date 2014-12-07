'''
Created on Dec 6, 2014

@author: Nelson Dos Santos
'''

import pygame
from person import Person


class Game:
    '''This class represents the game'''
    
    def __init__(self, resolution, title, bg, fps=30, playlist=[]):
        if type(resolution) != tuple or len(resolution) != 2:
            raise TypeError('unacceptable value for resolution')
        if type(title) != str:
            raise TypeError('title is not a str object')
        if type(bg) != tuple or len(bg) < 3 or len(bg) > 4:
            raise TypeError('incorrect value for bg')
        if type(fps) != int or fps < 0:
            raise TypeError('incorrect value for fps')
        if type(playlist) != list:
            raise TypeError('playlist not of type list')
        if len(playlist) > 0:
            for s in playlist:
                if type(s) != str:
                    raise TypeError('sound in playlist is not a str')
        
        self.title = title
        self.bg = bg
        self.fps = fps
        self.resolution = resolution
        self.surface = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption(self.title)
        self.surface.fill(self.bg)
        self.playlist = playlist
        self.width = self.resolution[0]
        self.height = self.resolution[1]
        self.clock = pygame.time.Clock()
        self.clock.tick(self.fps)
        self.moto_sounds = [pygame.mixer.Sound('sounds/accelerating.wav'), pygame.mixer.Sound('sounds/braking.wav')]
        self.moto_sounds[1].set_volume(0.02)
        self.moto_sounds[0].set_volume(0.5)
        # variable used to check the main loop condition
        self.running = False

        # list to hold the players
        self.players = []
        self.players.append(Person(self.surface, 'ncycle', 'images/cycle.png', (35, 70), 
                                   (int(self.resolution[0]/2) + 50, int(self.resolution[1]/2)), 6))

        self.back = pygame.image.load('images/board.jpeg')
        self.back_pos = [0, 0]
        
        pygame.display.update()
        self.run()
    #
    
    def show_players(self):
        for p in self.players:
            p.appear()
    #
    
    def are_players_crashing(self):
        for p in self.players:
            if p.crashing():
                return True
        return False
    #
    
    def run(self):
        self.running = True
        
        while self.running:            
            # events loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                # start walking
                if event.type == pygame.KEYDOWN:
                    
                    # move the player (ahead or back) in the current direction
                    if event.key == pygame.K_w: # go ahead
                        self.players[0].move()
                        self.moto_sounds[0].play()
                    elif event.key == pygame.K_s: # go back
                        self.players[0].brake()
                        self.moto_sounds[0].stop()
                        self.moto_sounds[1].play()
                        
                    # set the direction
                    if event.key == pygame.K_UP:
                        self.players[0].set_direction(0)
                    elif event.key == pygame.K_DOWN:
                        self.players[0].set_direction(1)
                    elif event.key == pygame.K_LEFT:
                        self.players[0].set_direction(2)
                    elif event.key == pygame.K_RIGHT:
                        self.players[0].set_direction(3)
     
                # brake walking
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.players[0].brake()
                        self.moto_sounds[0].stop()
                        self.moto_sounds[1].play()

            self.surface.blit(self.back, self.back_pos)
            
            self.players[0].goto(self.players[0].x + self.players[0].x_speed, 
                                 self.players[0].y + self.players[0].y_speed)
            
            self.surface.fill(self.bg)
            self.surface.blit(self.back, self.back_pos)
            self.show_players()
            
            if self.are_players_crashing():
                self.running = False

            
            pygame.display.update()
                       
#

        
