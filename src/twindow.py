"""
In particular, I would like to thank Samuel Trindade
for his suggestions for the design of the window :D

I want to thank also my team, who is always suggesting new things,
from which I learn a lot!


@author: Nelson Dos Santos, Sami Rami
"""

import tkinter
import pygame
import os


class TWindow(tkinter.Frame):
    
    """ Docs"""
    def __init__(self, root, title):
        super(TWindow, self).__init__()
        
        self.normal_font = ("arial", 20)
        self.over_font = ("arial", 22, 'bold')

        # ROOT
        self.root = root
        # Tell pygame's SDL window which window ID to use    
        os.environ['SDL_WINDOWID'] = str(self.winfo_id())
        # Show the window so it's assigned an ID.
        self.root.update()

        # initilizing pygame modules to have the mixer (maybe I can just import the mixer?)
        pygame.init()

        # WINDOW SETUP
        self.title = title
        self.root.title(self.title)
        self.width = 700
        self.height = 480
        pos = self.get_center_coords(self.width, self.height)
            
        self.root.geometry("{0}x{1}+{2}+{3}".format(self.width, self.height, pos[0], pos[1]))
        self.root.config(background='black')
        self.root.resizable(0, 0)

        # HEAD
        self.title_frame = self.get_panel(self.width, 50, color="black", fill=tkinter.X, expand=False)
        self.title_img = self.get_title_img()
        self.title_lab = tkinter.Label(self.title_frame, relief=tkinter.SUNKEN, bg="#000", image=self.title_img)
        self.title_lab.pack(fill=tkinter.BOTH)

        # BODY
        self.body_frame = self.get_panel(self.width, self.height, color='black', pady=60)

        # BUTTONS
        self.buttons = [self.get_button('Play'), self.get_button('Instructions'), self.get_button('Options')]

        # MUSIC
        self.mouse_over_btn_sound = pygame.mixer.Sound('src/sounds/buttons/mouse_over_button_sound.wav')

        
        # WINDOWS SETTINGS
        # put window as top window
        self.root.lift()
        self.root.call('wm', 'attributes', '.', '-topmost', True)
        self.root.after_idle(self.root.call, 'wm', 'attributes', '.', '-topmost', False)       
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

    def get_button(self, text, pady=25):
        btn = tkinter.Button(self.body_frame, text=text, width=25, bg='#2ff', font=self.normal_font)
        btn.bind('<Enter>', self.on_mouse_over_btn)
        btn.bind('<Leave>', self.on_mouse_leave_btn)
        btn.pack(ipady=3, pady=pady)
        return btn
    #
    
    def on_mouse_over_btn(self, event):
        event.widget.config(font=self.over_font)
        self.mouse_over_btn_sound.play()
    #
        
    def on_mouse_leave_btn(self, event):
        event.widget.config(font=self.normal_font)
        self.mouse_over_btn_sound.stop()
    #
    
# end of TWindow


class Panel(tkinter.Frame):
    def __init__(self, root, w, h, color='#000'):
        tkinter.Frame.__init__(self, root, width=w, height=h, background=color)

# end of TPanel

def test():
    """ Use this function to test the GUI for the Tron Kart game"""
    root = tkinter.Tk()
    tronwin = TWindow(root, 'Tron Kart')
    root.mainloop()
    pygame.quit()
#
#test()


                     



    
