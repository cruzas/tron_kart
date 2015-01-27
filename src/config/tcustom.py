"""
customisable settings for the Tron Kart game
this file can be modified
"""

import pygame
import random
from src.tutilities import get_file_names
from src.tcolors import *


# constants
COLORS = (BLUE, CYAN, GREEN, GREY, PINK, RED, YELLOW)
POWER_UPS = ('SPEED_UP', 'TRAIL_INC', 'RANDOM_BLUE', 'RANDOM_RED')
PLAYERS_IMGS = []
P_PATH = 'src/images/players/'

# loading images
for p in get_file_names(P_PATH, '.png'):
    if type(p) == str:
        PLAYERS_IMGS.append(P_PATH + p)
        
if len(PLAYERS_IMGS) != len(COLORS):
    raise ValueError('fatal error loading images')

# resolution
RES = (800, 450)
FULL_SCREEN = False
SAVING = False

# players: colors
randcolour1 = random.randint(0, len(COLORS) - 1)
randcolour2 = random.randint(0, len(COLORS) - 1)
while randcolour2 == randcolour1:
    randcolour2 = random.randint(0, len(COLORS) - 1)

# players: commands
P1_CMDS = {'up': pygame.K_w,
           'down':pygame.K_s,
           'left': pygame.K_a,
           'right': pygame.K_d,
           'stop': pygame.K_e}

PLAYER_1 = {'name': 'Kill Bill (S. Jobs)',
            'image': PLAYERS_IMGS[randcolour1],
            'color': COLORS[randcolour1],
            'commands': P1_CMDS}

P2_CMDS = {'up': pygame.K_UP,
           'down': pygame.K_DOWN,
           'left': pygame.K_LEFT,
           'right': pygame.K_RIGHT,
           'stop': pygame.K_RSHIFT}

PLAYER_2 = {'name': 'Bill Logical Gate',
            'image': PLAYERS_IMGS[randcolour2],
            'color': COLORS[randcolour2],
            'commands': P1_CMDS}

# keys' names
KEYS = {pygame.K_w: "W", pygame.K_s: "S", pygame.K_a: "A",
        pygame.K_d: "D", pygame.K_e: "E", pygame.K_UP: "Up arrow",
        pygame.K_DOWN: "Down arrow", pygame.K_LEFT: "Left arrow",
        pygame.K_RIGHT: "Right arrow", pygame.K_RSHIFT: "Right shift"}

# audio and music
VOLUME = 0
B_M_PATH = 'src/sounds/background/'
BACK_MUSIC = []

AIFF = get_file_names(B_M_PATH, '.aiff')
if len(AIFF) > 0:
    for m in AIFF:
        if type(m) == str:
            BACK_MUSIC.append(B_M_PATH + m)
    
WAV = get_file_names(B_M_PATH, '.wav')
if len(WAV) > 0:
    for m in WAV:
        if type(m) == str:
            BACK_MUSIC.append(B_M_PATH + m)

