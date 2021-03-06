"""
Authors: Tron Team
Creation: 27.01.2015
Last update: 27.01.2015
Description: TTimer is an utility class for timing certain events
in the Tron Kart game
"""

from pygame import *


KEYS = {
K_BACKSPACE: 'Backspace',
K_TAB: 'Tab',
K_CLEAR: 'Clear',
K_RETURN: 'Return',
K_PAUSE: 'Pause',
K_ESCAPE: 'Escape',
K_SPACE: 'Space',
K_EXCLAIM: 'Exclaim',
K_QUOTEDBL: 'Quotedbl',
K_HASH: 'Hash',
K_DOLLAR: 'Dollar',
K_AMPERSAND: 'Ampersand',
K_QUOTE: 'Quote',
K_LEFTPAREN: 'Left parenthesis',
K_RIGHTPAREN: 'Right parenthesis',
K_ASTERISK: 'Asterisk',
K_PLUS: 'Plus sign',
K_COMMA: 'Comma',
K_MINUS: 'Minus sign',
K_PERIOD: 'Period',
K_SLASH: 'Forward slash',
K_0: '0',
K_1: '1',
K_2: '2',
K_3: '3',
K_4: '4',
K_5: '5',
K_6: '6',
K_7: '7',
K_8: '8',
K_9: '9',
K_COLON: 'Colon',
K_SEMICOLON: 'Semicolon',
K_LESS: 'Less-than sign',
K_EQUALS: 'Equals sign',
K_GREATER: 'Greater-than sign',
K_QUESTION: 'Question mark',
K_AT: 'At',
K_LEFTBRACKET: 'Left bracket',
K_BACKSLASH: 'Backslash',
K_RIGHTBRACKET: 'Right bracket',
K_CARET: 'Caret',
K_UNDERSCORE: 'Underscore',
K_BACKQUOTE: 'Grave',
K_a: 'A',
K_b: 'B',
K_c: 'C',
K_d: 'D',
K_e: 'E',
K_f: 'F',
K_g: 'G',
K_h: 'H',
K_i: 'I',
K_j: 'J',
K_k: 'K',
K_l: 'L',
K_m: 'M',
K_n: 'N',
K_o: 'O',
K_p: 'P',
K_q: 'Q',
K_r: 'R',
K_s: 'S',
K_t: 'T',
K_u: 'U',
K_v: 'V',
K_w: 'W',
K_x: 'X',
K_y: 'Y',
K_z: 'Z',
K_DELETE: 'Delete',
K_KP0: 'Keypad 0',
K_KP1: 'Keypad 1',
K_KP2: 'Keypad 2',
K_KP3: 'Keypad 3',
K_KP4: 'Keypad 4',
K_KP5: 'Keypad 5',
K_KP6: 'Keypad 6',
K_KP7: 'Keypad 7',
K_KP8: 'Keypad 8',
K_KP9: 'Keypad 9',
K_KP_PERIOD: 'Keypad period',
K_KP_DIVIDE: 'Keypad divide',
K_KP_MULTIPLY: 'Keypad multiply',
K_KP_MINUS: 'Keypad minus',
K_KP_PLUS: 'Keypad plus',
K_KP_ENTER: 'Keypad enter',
K_KP_EQUALS: 'Keypad equals',
K_UP: 'Up arrow',
K_DOWN: 'Down arrow',
K_RIGHT: 'Right arrow',
K_LEFT: 'Left arrow',
K_INSERT: 'Insert',
K_HOME: 'Home',
K_END: 'End',
K_PAGEUP: 'Page up',
K_PAGEDOWN: 'Page down',
K_F1: 'F1',
K_F2: 'F2',
K_F3: 'F3',
K_F4: 'F4',
K_F5: 'F5',
K_F6: 'F6',
K_F7: 'F7',
K_F8: 'F8',
K_F9: 'F9',
K_F10: 'F10',
K_F11: 'F11',
K_F12: 'F12',
K_F13: 'F13',
K_F14: 'F14',
K_F15: 'F15',
K_NUMLOCK: 'Numlock',
K_CAPSLOCK: 'Capslock',
K_SCROLLOCK: 'Scrollock',
K_RSHIFT: 'Right shift',
K_LSHIFT: 'Left shift',
K_RCTRL: 'Right ctrl',
K_LCTRL: 'Left ctrl',
K_RALT: 'Right alt',
K_LALT: 'Left alt',
K_RMETA: 'Right meta',
K_LMETA: 'Left meta',
K_LSUPER: 'Left windows key',
K_RSUPER: 'Right windows key',
K_MODE: 'Mode shift',
K_HELP: 'Help',
K_PRINT: 'Print screen',
K_SYSREQ: 'Sysrq',
K_BREAK: 'Break',
K_MENU: 'Menu',
K_POWER: 'Power',
K_EURO: 'Euro'
}
