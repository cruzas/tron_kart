"""
In particular, I would like to thank Samuel Trindade
for his suggestions for the design of the window :D

@authors: Nelson Dos Santos, Sami Rami
"""

import tkinter
from tkinter import messagebox
import pygame
import os
from src.ttable import TTable


class TWindow(tkinter.Frame):

    """ TWindow is a class specifically created for the Tron Kart game."""

    proceed = True
    toplevels = [False, False] # 0=instructions, 1=options
    BG_COLOR = 'black'
    FONT = 'giorgia'
    NORMAL_FONT = (FONT, 20)    
    OVER_FONT = (FONT, 22, 'bold')

    C_NORMAL_FONT = (FONT, 16)
    C_OVER_FONT = (FONT, 20, 'bold')


    def __init__(self, root, title):
        super(TWindow, self).__init__()

        # ROOT
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
        self.root.config(background=TWindow.BG_COLOR)
        self.root.resizable(0, 0)

        # HEAD
        self.title_frame = self.get_panel(self.width, 50, color=TWindow.BG_COLOR, fill=tkinter.X, expand=False)
        self.title_img = self.get_title_img()
        self.title_lab = tkinter.Label(self.title_frame, relief=tkinter.SUNKEN, bg="#000", image=self.title_img)
        self.title_lab.pack(fill=tkinter.BOTH)

        # BODY
        self.body_frame = self.get_panel(self.width, self.height, color=TWindow.BG_COLOR, pady=60)

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

    #

    def on_exit(self):
        if messagebox.askyesno("Exit", "Do you want to quit the application?"):
            self.root.destroy()
            TWindow.proceed = False
    #
    
    def on_play_click(self, event):
        self.root.destroy()
        TWindow.proceed = True
    #

    def on_instructions_click(self, event):
        if not TWindow.toplevels[0]:
            TWindow.toplevels[0] = True
            top_level = tkinter.Toplevel(self.root, bg=TWindow.BG_COLOR)
            top_level.wm_title('Instructions')
            top_level.resizable(0, 0)
            width = 300
            height = int(self.root.winfo_height() / 2)
            x = self.root.winfo_x() - width
            y = self.root.winfo_y() 
            top_level.geometry('{0}x{1}+{2}+{3}'.format(width, height, x, y))
            instructions = Instructions(top_level, self.btn_sound)
    #
    
    def on_options_click(self, event):
        if not TWindow.toplevels[1]:
            TWindow.toplevels[1] = True
            top_level = tkinter.Toplevel(self.root, background=TWindow.BG_COLOR)
            top_level.wm_title('Options')
            top_level.resizable(0, 0)
            width = 300
            height = int(self.root.winfo_height() / 2)
            x = self.root.winfo_x() + self.root.winfo_width()
            y = self.root.winfo_y()
            top_level.geometry('{0}x{1}+{2}+{3}'.format(width, height, x, y))
            options = Options(top_level, self.btn_sound)
    #
    
    def get_panel(self, w, h, color='#000', fill="both", expand=True, pady=0):
        """ Gets and packs a new Panel object"""
        panel = Panel(self.root, w, h, color)
        panel.pack(fill=fill, expand=expand, pady=pady)
        return panel
    #

    def get_center_coords(self, width, height):
        """ Returns the coordinates to put a root in the middle of the screen"""
        return (int(self.root.winfo_screenwidth()/2 - width/2), int(self.root.winfo_screenheight()/2 - height/2))
    #
    
    def get_title_img(self):
        """ Returns an PhotoImage object for the title"""
        img = tkinter.PhotoImage(file='src/images/logos/tk_logo.gif')
        return img
    #

    def get_button(self, text, event_handler, pady=25):
        btn = tkinter.Button(self.body_frame, text=text, width=25, bg='#2ff', font=TWindow.NORMAL_FONT)
        btn.bind('<Enter>', self.on_mouse_over_btn)
        btn.bind('<Leave>', self.on_mouse_leave_btn)
        btn.bind('<Button-1>', event_handler)
        btn.pack(ipady=3, pady=pady)
        return btn
    #
    
    def on_mouse_over_btn(self, event):
        event.widget.config(font=TWindow.OVER_FONT)
        self.btn_sound.play()
    #
        
    def on_mouse_leave_btn(self, event):
        event.widget.config(font=TWindow.NORMAL_FONT)
        self.btn_sound.stop()
    #
    
# end of TWindow



class Panel(tkinter.Frame):
    
    def __init__(self, root, w, h, color='#000'):
        tkinter.Frame.__init__(self, root, width=w, height=h, background=color)
    #
    
# end Panel


class Options(tkinter.Frame):
    option_opened = False

    def __init__(self, root, btn_sound):
        super(Options, self).__init__()
        self.root = root
        self.root.wm_protocol("WM_DELETE_WINDOW", self.on_exit)
        self.btn_sound = btn_sound
        self.root.update()
        self.buttons = [self.get_button('Game Settings', self.game_settings),
                        self.get_button('Video Settings', self.video_settings),
                        self.get_button('Audio Settings', self.audio_settings)]
    #
    
    def on_exit(self):
        TWindow.toplevels[1] = False
        self.root.destroy()
    #

    def get_button(self, text, event_handler, pady=24):
        btn = tkinter.Button(self.root, text=text, width=15, bg='#2ff', font=TWindow.C_NORMAL_FONT)
        btn.bind('<Enter>', self.on_mouse_over_btn)
        btn.bind('<Leave>', self.on_mouse_leave_btn)
        btn.bind('<Button-1>', event_handler)
        btn.pack(ipady=1, pady=pady)
        return btn
    #
    
    def on_mouse_over_btn(self, event):
        event.widget.config(font=TWindow.C_OVER_FONT)
        self.btn_sound.play()
    #
        
    def on_mouse_leave_btn(self, event):
        event.widget.config(font=TWindow.C_NORMAL_FONT)
        self.btn_sound.stop()
    #

    def game_settings(self, event):
        print('game settings')
        self.root.withdraw()# hides the window

    def video_settings(self, event):
        print('video settings')
        self.root.withdraw()# hides the window

    def audio_settings(self, event):
        print('audio settings')
        self.root.withdraw() # hides the window
    
# end Instructions


class Instructions(tkinter.Frame):
    def __init__(self, root, btn_sound):
        super(Instructions, self).__init__()
        self.root = root
        self.root.wm_protocol("WM_DELETE_WINDOW", self.on_exit)
        self.btn_sound = btn_sound
        self.root.update()
        self.buttons = [self.get_button('Commands', self.commands),
                        self.get_button('Colors', self.colors),
                        self.get_button('Power Ups', self.power_ups)]
        
    def on_exit(self):
        TWindow.toplevels[0] = False
        self.root.destroy()

    def get_button(self, text, event_handler, pady=24):
        btn = tkinter.Button(self.root, text=text, width=15, bg='#2ff', font=TWindow.C_NORMAL_FONT)
        btn.bind('<Enter>', self.on_mouse_over_btn)
        btn.bind('<Leave>', self.on_mouse_leave_btn)
        btn.bind('<Button-1>', event_handler)
        btn.pack(ipady=1, pady=pady)
        return btn
    #
    
    def on_mouse_over_btn(self, event):
        event.widget.config(font=TWindow.C_OVER_FONT)
        self.btn_sound.play()
    #
        
    def on_mouse_leave_btn(self, event):
        event.widget.config(font=TWindow.C_NORMAL_FONT)
        self.btn_sound.stop()
    #

    def commands(self, event):
        print('commands')

    def colors(self, event):
        print('colors')

    def power_ups(self, event):
        print('power_ups')
    
# end Options


class Commands:

    def __init__(self, root, btn_sound):
        pass
#

class Colors:
    def __init__(self, root, btn_sound):
        pass
#

class PowerUps:
    def __init__(self, root, btn_sound):
        pass
        


                     



    
