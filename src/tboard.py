"""
Authors: Tron Team
Creation: December, 2014
Last update: 27.01.2015
Description: TBoard class which represents the board of Tron Kart game
"""

import pygame


class TBoard:
    """represents the board of a Tron Kart game"""
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

    def update(self):
        self.surface.fill(self.color)
        if self.using_img:
            self.surface.blit(self.image, (0, 0))

    def get_middle_coords(self, msg, font_size, bold=False, italic=False):
        """Returns the coordinates to put a centered message to the screen"""
        font = pygame.font.SysFont(None, font_size, bold, italic)
        text = font.render(msg, True, (0, 0, 0))
        rect = text.get_rect()
        return (self.width/2 - rect[2]/2, self.width/2 - rect[3]/2)

    def get_score_coords(self, msg, font_size, side="RIGHT", board_distance=10, bold=False, italic=False):
        font = pygame.font.SysFont(None, font_size, bold, italic)
        text = font.render(msg, True, (0, 0, 0))
        rect = text.get_rect()
        if side == "RIGHT":
            return (self.width - board_distance - rect[2], board_distance)
        elif side == "LEFT": # quite useless
            return (board_distance, board_distance)
    
    def write(self, msg, color, font_size, pos='CENTER', bold=False, italic=False):
        """This function writes some text in the self.surface."""
        font = pygame.font.SysFont(None, font_size, bold, italic)
        text = font.render(msg, True, color)
        
        if pos == 'CENTER':
            rect = text.get_rect()
            x = self.width/2 - rect[2]/2
            y = self.height/2 - rect[3]/2
            self.surface.blit(text, [x, y])
        else:
            self.surface.blit(text, pos)
