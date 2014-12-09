'''
See example of a Cocos2D class.
Make sure you have cocos2d for Python3.4 installed.
'''


import cocos

class window(cocos.layer.Layer):
    def __init__(self):
        super(window, self).__init__()

        label = cocos.text.Label('Hello, world', font_name='Times New Roman',
                                 font_size=32, anchor_x='center',
                                 anchor_y='center')
        self.add(label)
        label.position = 320, 240
        
cocos.director.director.init()

win = window()

main_scene = cocos.scene.Scene(win)
cocos.director.director.run(main_scene)

## GitHub repo Test
