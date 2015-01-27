"""
AUTHOR: Nelson Dos Santos
COMMENT: Make sure you have cocos2d installed for Python 3x
"""

import cocos


class Window(cocos.layer.Layer):
    def __init__(self):
        super(Window, self).__init__()

        label = cocos.text.Label('Hello, world', font_name='Times New Roman', font_size=32, anchor_x='center', anchor_y='center')
        self.add(label)
        # print(self)
        label.position = 320, 240
        
    def print_(self):
        print("I am a window")

cocos.director.director.init()

win3 = Window()
win3.print_()

main_scene = cocos.scene.Scene(win3)
cocos.director.director.run(main_scene)




