"""
customisable settings for the Tron Kart game
this file can be modified
"""

import pygame
import random
from src.utils.tutilities import get_file_names
from src.utils.tcolors import *


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

PLAYER_1 = {'name': 'S. Jobs',
            'image': PLAYERS_IMGS[randcolour1],
            'color': COLORS[randcolour1],
            'commands': P1_CMDS}

P2_CMDS = {'up': pygame.K_UP,
           'down': pygame.K_DOWN,
           'left': pygame.K_LEFT,
           'right': pygame.K_RIGHT,
           'stop': pygame.K_RSHIFT}

PLAYER_2 = {'name': 'B. Gates',
            'image': PLAYERS_IMGS[randcolour2],
            'color': COLORS[randcolour2],
            'commands': P1_CMDS}

import src.utils.pygamekeys as pygamekeys
KEYS = pygamekeys.KEYS

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

#
I_M_PATH = 'src/sounds/intro/'
INTRO_MUSIC = []
