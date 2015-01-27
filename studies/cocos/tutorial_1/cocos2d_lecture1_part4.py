"""
AUTHOR: Nelson Dos Santos
LECTURE 1 (PART 4) - HANDLING EVENTS
TOPICS:
    1. Classes
    2. Objects
    3. ACTIONS: Scaling and Rotating!
    
COMMENT: If you don't understand something, you should ask me immediately,
and I will try to answer in the best way I can. This OOP paradigm will be used
a lot in the next semester, so if you learn it now, you will be more confortable.
If we don't finish the game, ok,
but at least we are trying to learn something very USEFUL !!

I hope you like to learn this, and don't hesitate, again, to ask me for help!!!

YOU SHOULD TRY TO IMPLEMENT WHAT IS IN THIS SCRIPT BY YOURSELF!!!!
"""

import cocos  # NEVER FORGET TO IMPORT THE GOD MODULE

import pyglet  # BE SURE TO IMPORT ALSO THIS MODULE!!!



# HANDLING EVENTS, FOR EXAMPLE MEETING A GIRL

# What is an event? An event is what you know an event is.
# Example, if you don't remember: the press of a key or of the mouse,...

# Yes, we have to handle the event. What does it mean?
# We have to determine what happens when the user clicks a key of the keyword
# For example, we could handle that event (press of a key)
# calling a function that writes the key to the screen, nice uhm?

# Usually, to handle an event, we say that we "listen" to that event,
# otherwise we cannot handle it.
# Usually, we handle an event with a function that "waits" until
# that event happens.

# Ok, in Cocos, we have to listen to 'director.window' events.

# What is going to be the listener? cocos.layer, which can 'automatically'
# listen to 'director.window 'events

# So, do you still remember where did we use this 'cocos.layer'?
# We use 'layers' for as 'mother' classes for our classes

# In our layer subclass, set the 'is_event_handler' class member to True
# And our friend Cocos will take care of the situation :D

# Now, that we have an introduction of what an EVENT is and what is an EVENT HANDLER,
# we are going to build step by step a simple game that shows
# which keys are pressed and that reacts to the mouse motion and clicks.

# This game has a scene with 2 layers:
# 1. shows which keys are currently pressed (how many times they are pressed)
# 2. shows the text with the mouse position, and clicking, moves the text.

# OK, let's define our new class MouseDisplayer, which derives from 'Layer'.



class MouseDisplayer(cocos.layer.Layer):
    is_event_handler = True  # Make this class handle events.

    # CONSTRUCTOR:

    def __init__(self):
        # Initializing part of the super class (properties) calling the constructor of the super class.
        super(MouseDisplayer, self).__init__()

        self.posx = 100
        self.posy = 240
        self.text = cocos.text.Label("No mouse events yet", font_size=18,
                                     x=self.posx, y=self.posy)
        self.add(self.text)


    # Function that update the text of the Label
    def update_text(self, x, y):
        text = "Mouse {0}, {1}".format(x, y)

        self.text.element.text = text
        self.text.element.x = self.posx
        self.text.element.y = self.posy


    # Adding EVENT HANDLERS to handle events (mouse click or motion...)

    """Called when the mouse moves over the app window with no button pressed

    (x, y) are the physical coordinates of the mouse
    (dx, dy) is the distance vector covered by the mouse pointer since the
      last call.
    """

    def on_mouse_motion(self, x, y, dx, dy):
        self.update_text(x, y)


    """Called when the mouse moves over the app window with some button(s) pressed

      (x, y) are the physical coordinates of the mouse
      (dx, dy) is the distance vector covered by the mouse pointer since the
        last call.
      'buttons' is a bitwise or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
      'modifiers' is a bitwise or of pyglet.window.key modifier constants
         (values like 'SHIFT', 'OPTION', 'ALT')
      """


    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.posx, self.posy = x, y
        self.update_text(x, y)


    """This function is called when any mouse button is pressed

    (x, y) are the physical coordinates of the mouse
    'buttons' is a bitwise or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
    'modifiers' is a bitwise or of pyglet.window.key modifier constants
       (values like 'SHIFT', 'OPTION', 'ALT')
    """

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.posx, self.posy = cocos.director.director.get_virtual_coordinates(x, y)
        self.update_text(x, y)

        # COCOS has 2 coordinates systems, a physical one and a virtual one.
        # The mouse event handlers (the function defined above)
        # receive their arguments from pyglet in physical coordinates

        # If you want to map that to virtual coordinates, you need to use the
        # director.get_virtual_coordinates method, which does the correct mapping.

        # If you put instead self.posx, self.posy = x, y in the 'on_mouse_press' handler above,
        # you will see that the app seems to work, but if you resize the window, the
        # clicks will move the next to the wrong place.

        # For completness, they are other mouse event that can be of interest:

        # on_mouse_release
        # on_mouse_scroll
        # on_mouse_leave: called when the mouse goes out of the window
        # on_mouse_enter: called when the mouse cursor enters the window  # END of the class.


# HOUSE KEEPING STUFF
cocos.director.director.init(resizable=True)

mouse_displayer = MouseDisplayer()

main_scene = cocos.scene.Scene(mouse_displayer)

cocos.director.director.run(main_scene)




