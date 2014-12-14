"""
DO NOT TOUCH THIS FILE!
THIS IS JUST A BACKUP FILE!!!!
"""

import pygame
from src.tutilities import get_file_names
from src.tcolors import *

#############################################################################
# CONSTANTS => DO NOT CHANGE THIS PART!!!
COLORS = (BLUE, CYAN, GREEN, GREY, PINK, RED, YELLOW)

POWER_UPS = ('SPEED_UP', 'TRAIL_INC', 'RANDOM_BLUE', 'RANDOM_RED')

PLAYERS_IMGS = []

P_PATH = 'src/images/players/'

for p in get_file_names(P_PATH, '.png'):
    if type(p) == str:
        PLAYERS_IMGS.append(P_PATH + p)
        
if len(PLAYERS_IMGS) != len(COLORS):
    raise ValueError('fatal error loading images')

#############################################################################
#############################################################################
# STANDARD SETTINGS
# VIDEO
RES = (800, 450)
FULL_SCREEN = False

#############################################################################
# GAME
SAVING = False
P1_CMDS = {'up': pygame.K_w,
           'down':pygame.K_s,
           'left': pygame.K_a,
           'right': pygame.K_d,
           'stop': pygame.K_e}

P1_KEY_NAMES = {}


PLAYER_1 = {'name': 'Kill Bill (S. Jobs)',
            'image': PLAYERS_IMGS[1],
            'color': COLORS[1],
            'commands': P1_CMDS}
#
P2_CMDS = {'up': pygame.K_UP,
           'down': pygame.K_DOWN,
           'left': pygame.K_LEFT,
           'right': pygame.K_RIGHT,
           'stop': pygame.K_RSHIFT}

PLAYER_2 = {'name': 'Bill Logical Gate',
            'image': PLAYERS_IMGS[5],
            'color': COLORS[5],
            'commands': P1_CMDS}

P2_KEY_NAMES = {}

#############################################################################
# AUDIO
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
                
#############################################################################

