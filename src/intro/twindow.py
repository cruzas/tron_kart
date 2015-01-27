"""
Authors: Nelson Brochado, Sami Rami
Creation: December, 2014
Last Update: 27.01.2015
Description: introductory UI to the Tron Kart game

TODO:
 - finish Toplevels
 - fix eventual errors
 - improve performance
"""

import tkinter
from tkinter import messagebox
import pygame
import os
from src.intro.ttable import TTable
from src.intro.constants import *
from src.config.tcustom import *


class TWindow(tkinter.Frame):
    """ TWindow is a class specifically created for the Tron Kart game."""
    proceed = True
    toplevels = [False, False] # 0=instructions, 1=options
    
    def __init__(self, root, title):
        super(TWindow, self).__init__()
        
        self.root = root
        # Tell pygame's SDL window which window ID to use    
        os.environ['SDL_WINDOWID'] = str(self.winfo_id())
        # Show the window so it's assigned an ID.
        #self.root.update() # show for a moment another small window at the left
        
        TWindow.destroyed = False
        # initilizing pygame modules to have the mixer (maybe I can just import the mixer?)
        pygame.init()

        # WINDOW SETUP
        self.title = title
        self.root.title(self.title)
        self.width = 700
        self.height = 480
        self.pos = self.get_center_coords(self.width, self.height)
            
        self.root.geometry("{0}x{1}+{2}+{3}".format(self.width, self.height, self.pos[0], self.pos[1]))
        self.root.config(background=BG_COLOR)
        self.root.resizable(0, 0)

        # HEAD
        self.title_frame = self.get_panel(self.width, 50, color=BG_COLOR, fill=tkinter.X, expand=False)
        self.title_img = self.get_title_img()
        self.title_lab = tkinter.Label(self.title_frame, relief=tkinter.SUNKEN, bg="#000", image=self.title_img)
        self.title_lab.pack(fill=tkinter.BOTH)

        # BODY
        self.body_frame = self.get_panel(self.width, self.height, color=BG_COLOR, pady=60)

        # BUTTONS
        self.buttons = [self.get_button('Play',  self.on_play_click),
                        self.get_button('Instructions', self.on_instructions_click),
                        self.get_button('Options', self.on_options_click)]

        # MUSIC
        self.btn_sound = pygame.mixer.Sound('src/sounds/buttons/mouse_over_button_sound.wav')

        # WINDOWS SETTINGS
        # put window as top window
        self.root.lift()
        self.root.call('wm', 'attributes', '.', '-topmost', True)
        self.root.after_idle(self.root.call, 'wm', 'attributes', '.', '-topmost', False)       

        # ON EXIT
        self.root.wm_protocol("WM_DELETE_WINDOW", self.on_exit)

    def on_exit(self):
        """docs"""
        if messagebox.askyesno("Exit", "Do you want to quit the application?"):
            self.root.destroy()
            TWindow.proceed = False
    
    def on_play_click(self, event):
        """docs"""
        self.root.destroy()
        TWindow.proceed = True

    def on_instructions_click(self, event):
        """docs"""
        if not TWindow.toplevels[0]:
            TWindow.toplevels[0] = True
            top_level = tkinter.Toplevel(self.root, bg=BG_COLOR)
            top_level.wm_title('Instructions')
            top_level.resizable(0, 0)
            width = 300
            height = int(self.root.winfo_height() / 2) - 12
            x = self.root.winfo_x() - width
            y = self.root.winfo_y() 
            top_level.geometry('{0}x{1}+{2}+{3}'.format(width, height, x, y))
            instructions = Instructions(top_level, self.btn_sound)
    
    def on_options_click(self, event):
        """docs"""
        if not TWindow.toplevels[1]:
            TWindow.toplevels[1] = True
            top_level = tkinter.Toplevel(self.root, background=BG_COLOR)
            top_level.wm_title('Options')
            top_level.resizable(0, 0)
            width = 300
            height = int(self.root.winfo_height() / 2) - 12
            x = self.root.winfo_x() + self.root.winfo_width()
            y = self.root.winfo_y()
            top_level.geometry('{0}x{1}+{2}+{3}'.format(width, height, x, y))
            options = Options(top_level, self.btn_sound)
    
    def get_panel(self, w, h, color='#000', fill="both", expand=True, pady=0):
        """ Gets and packs a new Panel object"""
        panel = Panel(self.root, w, h, color)
        panel.pack(fill=fill, expand=expand, pady=pady)
        return panel

    def get_center_coords(self, width, height):
        """ Returns the coordinates to put a root in the middle of the screen"""
        return (int(self.root.winfo_screenwidth()/2 - width/2), int(self.root.winfo_screenheight()/2 - height/2))
    
    def get_title_img(self):
        """ Returns an PhotoImage object for the title"""
        img = tkinter.PhotoImage(file='src/images/logos/tk_logo.gif')
        return img

    def get_button(self, text, event_handler, pady=25):
        """docs"""
        btn = tkinter.Button(self.body_frame, text=text, width=25, bg='#2ff', font=NORMAL_FONT)
        btn.bind('<Enter>', self.on_mouse_over_btn)
        btn.bind('<Leave>', self.on_mouse_leave_btn)
        btn.bind('<Button-1>', event_handler)
        btn.pack(ipady=3, pady=pady)
        return btn
    
    def on_mouse_over_btn(self, event):
        """docs"""
        event.widget.config(font=OVER_FONT)
        self.btn_sound.play()
        
    def on_mouse_leave_btn(self, event):
        """docs"""
        event.widget.config(font=NORMAL_FONT)
        self.btn_sound.stop()


class Panel(tkinter.Frame):
    """docs"""
    def __init__(self, root, w, h, color='#000'):
        """docs"""
        tkinter.Frame.__init__(self, root, width=w, height=h, background=color)


class Instructions(tkinter.Frame):
    """docs"""
    i_opened = False
    
    def __init__(self, root, btn_sound):
        """docs"""
        super(Instructions, self).__init__()
        self.root = root
        self.root.wm_protocol("WM_DELETE_WINDOW", self.on_exit)
        self.btn_sound = btn_sound
        self.root.update()
        self.buttons = [self.get_button('Commands', self.commands),
                        self.get_button('Colors', self.colors),
                        self.get_button('Power Ups', self.power_ups)]
        
    def on_exit(self):
        """docs"""
        TWindow.toplevels[0] = False
        self.root.destroy()

    def get_button(self, text, event_handler, pady=20):
        """docs"""
        btn = tkinter.Button(self.root, text=text, width=15, bg='#2ff', font=C_NORMAL_FONT)
        btn.bind('<Enter>', self.on_mouse_over_btn)
        btn.bind('<Leave>', self.on_mouse_leave_btn)
        btn.bind('<Button-1>', event_handler)
        btn.pack(ipady=1, pady=pady)
        return btn
    
    def on_mouse_over_btn(self, event):
        """docs"""
        event.widget.config(font=C_OVER_FONT)
        self.btn_sound.play()
        
    def on_mouse_leave_btn(self, event):
        """docs"""
        event.widget.config(font=C_NORMAL_FONT)
        self.btn_sound.stop()

    def commands(self, event):
        """docs"""
        if not Instructions.i_opened:
            Instructions.i_opened = True
            root = tkinter.Toplevel(self.root, bg=BG_COLOR)
            root.wm_title('Commands')
            # root.resizable(0, 0)
            width = self.root.winfo_width()
            height = self.root.winfo_height() + 1
            x = self.root.winfo_x()
            y = self.root.winfo_y() + height + 22
            root.geometry('{0}x{1}+{2}+{3}'.format(width, height, x, y))
            Commands(root, self.btn_sound)
            
    
    def colors(self, event):
        """docs"""
        if not Instructions.i_opened:
            Instructions.i_opened = True
            root = tkinter.Toplevel(self.root, bg=BG_COLOR)
            root.wm_title('Colors')
            root.resizable(0, 0)
            width = self.root.winfo_width()
            height = self.root.winfo_height() + 1
            x = self.root.winfo_x()
            y = self.root.winfo_y() + height + 22
            root.geometry('{0}x{1}+{2}+{3}'.format(width, height, x, y))
            colors = Colors(root, self.btn_sound)
    
    def power_ups(self, event):
        """docs"""
        if not Instructions.i_opened:
            Instructions.i_opened = True
            root = tkinter.Toplevel(self.root, bg=BG_COLOR)
            root.wm_title('Power Ups')
            root.resizable(0, 0)
            width = self.root.winfo_width()
            height = self.root.winfo_height() + 1
            x = self.root.winfo_x()
            y = self.root.winfo_y() + height + 22
            root.geometry('{0}x{1}+{2}+{3}'.format(width, height, x, y))
            power_ups = PowerUps(root, self.btn_sound)


class Commands(tkinter.Frame):
    """docs"""
    def __init__(self, root, btn_sound):
        """docs"""
        super(Commands, self).__init__(master=root)
        self.root = root
        self.btn_sound = btn_sound
        self.root.wm_protocol("WM_DELETE_WINDOW", self.on_exit)
        self.names = [PLAYER_1['name'][0:10], PLAYER_2['name'][0:10]]
        
        self.headers_1 = ['', self.names[0]]
        self.data_1 = [['COMMAND', 'NAME']]
        
        for k, v in P1_CMDS.items():               
            self.data_1.append([k.capitalize(), KEYS[v]])
            
        self.table = TTable(self, rows=6, cols=2, h_row=0, h_col=0,
                            headers=self.headers_1, data=self.data_1)
        self.table.grid(row=0, column=0, sticky='nsew')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.headers_2 = ['', self.names[1]]
        self.data_2 = [['COMMAND', 'NAME']]

        for k, v in P2_CMDS.items():               
            self.data_2.append([k.capitalize(), KEYS[v]])
            
        self.table = TTable(self, rows=6, cols=2, h_row=1, h_col=1,
                            headers=self.headers_2, data=self.data_2)
        self.table.grid(row=0, column=1, sticky='nsew')
        self.columnconfigure(1, weight=1)
        self.pack(expand=1, fill='both')
        
    def on_exit(self):
        """docs"""
        Instructions.i_opened = False
        self.root.destroy()


class Colors:
    """docs"""
    def __init__(self, root, btn_sound):
        self.root = root
        self.btn_sound = btn_sound
        self.root.wm_protocol("WM_DELETE_WINDOW", self.on_exit)
    
    def on_exit(self):
        """docs"""
        Instructions.i_opened = False
        self.root.destroy()


class PowerUps:
    """docs"""
    def __init__(self, root, btn_sound):
        self.root = root
        self.btn_sound = btn_sound
        self.root.wm_protocol("WM_DELETE_WINDOW", self.on_exit)
    
    def on_exit(self):
        """docs"""
        Instructions.i_opened = False
        self.root.destroy()
    

class Options(tkinter.Frame):
    """docs"""
    o_opened = False
    
    def __init__(self, root, btn_sound):
        super(Options, self).__init__()
        self.root = root
        self.root.wm_protocol("WM_DELETE_WINDOW", self.on_exit)
        self.btn_sound = btn_sound
        self.root.update()
        self.buttons = [self.get_button('Game Settings', self.game_settings),
                        self.get_button('Video Settings', self.video_settings),
                        self.get_button('Audio Settings', self.audio_settings)]
        
    def on_exit(self):
        """docs"""
        TWindow.toplevels[1] = False
        self.root.destroy()

    def get_button(self, text, event_handler, pady=20):
        """docs"""
        btn = tkinter.Button(self.root, text=text, width=15, bg='#2ff', font=C_NORMAL_FONT)
        btn.bind('<Enter>', self.on_mouse_over_btn)
        btn.bind('<Leave>', self.on_mouse_leave_btn)
        btn.bind('<Button-1>', event_handler)
        btn.pack(ipady=1, pady=pady)
        return btn
    
    def on_mouse_over_btn(self, event):
        """docs"""
        event.widget.config(font=C_OVER_FONT)
        self.btn_sound.play()
        
    def on_mouse_leave_btn(self, event):
        """docs"""
        event.widget.config(font=C_NORMAL_FONT)
        self.btn_sound.stop()

    def game_settings(self, event):
        """docs"""
        if not Options.o_opened:
            Options.o_opened = True
            root = tkinter.Toplevel(self.root, bg=BG_COLOR)
            root.wm_title('Game Settings')
            root.resizable(0, 0)
            width = self.root.winfo_width()
            height = self.root.winfo_height() + 1
            x = self.root.winfo_x()
            y = self.root.winfo_y() + height + 22
            root.geometry('{0}x{1}+{2}+{3}'.format(width, height, x, y))
            cmds = GameSettings(root, self.btn_sound)
    
    def video_settings(self, event):
        """docs"""
        if not Options.o_opened:
            Options.o_opened = True
            root = tkinter.Toplevel(self.root, bg=BG_COLOR)
            root.wm_title('Video Settings')
            root.resizable(0, 0)
            width = self.root.winfo_width()
            height = self.root.winfo_height() + 1
            x = self.root.winfo_x()
            y = self.root.winfo_y() + height + 22
            root.geometry('{0}x{1}+{2}+{3}'.format(width, height, x, y))
            colors = VideoSettings(root, self.btn_sound)
    
    def audio_settings(self, event):
        """docs"""
        if not Options.o_opened:
            Options.o_opened = True
            root = tkinter.Toplevel(self.root, bg=BG_COLOR)
            root.wm_title('Audio Settings')
            root.resizable(0, 0)
            width = self.root.winfo_width()
            height = self.root.winfo_height() + 1
            x = self.root.winfo_x()
            y = self.root.winfo_y() + height + 22
            root.geometry('{0}x{1}+{2}+{3}'.format(width, height, x, y))
            power_ups = AudioSettings(root, self.btn_sound)


class GameSettings:
    """docs"""
    def __init__(self, root, btn_sound):
        self.root = root
        self.btn_sound = btn_sound
        self.root.wm_protocol("WM_DELETE_WINDOW", self.on_exit)
    
    def on_exit(self):
        Options.o_opened = False
        self.root.destroy()


class VideoSettings:
    """docs"""
    def __init__(self, root, btn_sound):
        self.root = root
        self.btn_sound = btn_sound
        self.root.wm_protocol("WM_DELETE_WINDOW", self.on_exit)
    
    def on_exit(self):
        Options.o_opened = False
        self.root.destroy()


class AudioSettings:
    """docs"""
    def __init__(self, root, btn_sound):
        self.root = root
        self.btn_sound = btn_sound
        self.root.wm_protocol("WM_DELETE_WINDOW", self.on_exit)
    
    def on_exit(self):
        Options.o_opened = False
        self.root.destroy()


def test():
    pass

if __name__ == '__main__':
    test()
