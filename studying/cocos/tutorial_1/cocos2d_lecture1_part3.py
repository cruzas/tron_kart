"""
AUTHOR: Nelson Dos Santos
LECTURE 1 (PART 3) - HANDLING EVENTS
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

# Now, that we have an intruduction of what an EVENT is and what is an EVEND HANDLER,
# we are going to build step by step a simple game that shows
# which keys are pressed and that reacts to the mouse motion and clicks.

# This game has a scene with 2 layers:
# 1. shows which keys are currently pressed (how many times they are pressed)
# 2. shows the text with the mouse position, and clicking, moves the text.

# OK, let's define our new class KeyDisplay, which derives from 'Layer'.

class KeyDisplay(cocos.layer.Layer):
    # If you want that your layer receives director.window events
    # you must set this variable to 'True' (COPYRIGHT)

    is_event_handler = True

    # CONSTRUCTOR or INITIALIZER of this class
    # DONT FORGET self AS FIRST PARAMETER FOR EACH METHOD AND ATTRIBUTE FOR THE CLASS

    def __init__(self):
        # Calling the constructor of the mother class...
        # Why do we need to call the constructor of the 'mother' class?
        # Because, since we "inherit" or "derived" from 'Layer' (from another class)
        # We receive every single 'attribute' and 'function' from it.
        # So we can say that KeyDisplay is a 'Layer', but not vice-versa :D
        # Note that we pass the name of the current class to the super class
        # and we pass also 'self'.
        super(KeyDisplay, self).__init__()

        # Creating a MUSIC LABEL object
        self.text = cocos.text.Label("", x=100, y=280)

        # To keep track of which keys are pressed:

        # set function creates a data structure of type set()
        # This 'set' is going to hold the keys pressed at any given time.
        self.keys_pressed = set()

        self.update_text()  # Method that I will create after __init__

        # Adding self.text to this class (KeyDisplay, which derives from Layer)
        self.add(self.text)

    # END OF __init__

    def update_text(self):  # Note that also this function receives 'self' as parameter
        key_names = ''

        for k in self.keys_pressed:  # Defined in the constructor
            key_names += pyglet.window.key.symbol_string(k)

        text = 'Keys: ' + ', '.join(key_names)  # join basically puts the comma between all 'key_names'

        # Now, we want to update the self.text:
        # So, how do we call a property of a class? We use self.name_of_property!
        self.text.element.text = text

    # Now, we need to add EVENT HANDLERS to the Layer (this class: KeyDisplay)
    # How do we add EVENT HANDLERS to this class?
    # Well, we just have to add methods some methods called
    # usually something like this: 'on_mouse_blah' or 'on_key_bleh'
    # Now, let's talk about 2 real EVENT HANDLERS: on_key_press or on_key_release

    # END of update_text


    """This function is called when a key is pressed.
    'key' is a constant indicating which key was pressed.
    'modifiers' is a bitwise or of several constants indicating which
        modifiers are active at the time of the press (ctrl, shift, capslock, etc.)
    """

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        # Adding to the set 'self.keys_pressed'
        # the constant representing the 'key' pressed.
        self.update_text()  # We call this method (function of a class)
        # to update the text of the Label.

    # END of the EVENT HANDLER on_key_pressed

    def on_key_release(self, key, modifiers):
        """This function is called when a key is released.

    'key' is a constant indicating which key was pressed.
    'modifiers' is a bitwise or of several constants indicating which
        modifiers are active at the time of the press (ctrl, shift, capslock, etc.)

    Constants are the ones from pyglet.window.key
    """
        self.keys_pressed.remove(key)
        self.update_text()

        # This 2 functions are the reverse of 1 another (in this case, but we cannot use them to handle the events in other ways!).
        # In fact, 'on_key_pressed' adds the key pressed to the self.keys_pressed set,
        # and 'on_key_release' removes the key being release from the same set!

        # END of the EVENT HANDLER on_key_release

# END of the CLASS


# Let's create our usual environment to see a window

cocos.director.director.init()

key_displayer = KeyDisplay()

# Creating the scene where to put out class KeyDisplay

main_scene = cocos.scene.Scene(key_displayer)

cocos.director.director.run(main_scene)
