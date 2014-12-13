"""
AUTHOR: Nelson Dos Santos
COMMENT: Make sure you have cocos2d installed for Python 3x
DESCRIPTION: How to create a menu
"""

import cocos

# Scene = Screen = Stage
# Many screen, but just 1 active at a certain time.

# Example of a game with scenes: Intro, Menu, Level 1, Cutscene 1, Level 1,
# Winning cutscene, losing cutscene, high scores screen.

# Scenes (more or less) as separate apps
                   
class TronMenu(cocos.menu.Menu):

    is_event_handler = True

    def __init__(self):
        super(TronMenu, self).__init__()
        self.m_items = []
        self.m_items.append(cocos.menu.MenuItem('New', self.on_new_game))
        self.m_items.append(cocos.menu.MenuItem('Quit', self.on_quit))
        self.m_items.append(cocos.menu.ToggleMenuItem('Score', self.score, cocos.director.director.show_FPS))

        self.volumes = ['Mute','10','20','30','40','50','60','70','80','90','100']

        self.m_items.append(cocos.menu.MultipleMenuItem('Volume', self.volume, self.volumes, 8))
        self.create_menu(self.m_items, cocos.menu.zoom_in(), cocos.menu.zoom_out())        
    #

    def volume(self):
        print("Volume!")
    #
    
    def on_new_game(self):
        print("New game!")
    #

    def on_quit(self):
        cocos.sys.exit(0)
    #

    def score(self):
        print("Score")
    #
# END

# Setting up the window

cocos.director.director.init()  # Initializes everything.

menu = TronMenu()

scene = cocos.scene.Scene(menu)

cocos.director.director.run(scene)
