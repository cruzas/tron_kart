"""
AUTHOR: Nelson Dos Santos
LECTURE 1 - Learn how to create a simple window!
TOPICS:
    1. Classes
    2. Objects
    3. __init__
    4. Classes that derive from other classes
    5. The keyword 'self' to refer to the current object (to its methods and attributes)
    6. super()
    7. Create our own class (Window)
    8. Create the real window where (that your class will modify)
    9. Create a Scene where you are going to put the your object (of type Window)
    10. Run all the window and the graphics (asking to a director)

COMMENT: If you don't understand something, you should ask me immediately,
and I will try to answer is the best way I can. This OOP paradigm will help be used
always the next semester, so if you learn it now, you will be more confortable.
If we don't finish the game, ok, but at least we are trying to learn something very useful!!

I hope you like to learn this, and don't hesitate, again, to ask me for help!!!
"""

import cocos

# Window is a class that derives from 'cocos.layer.Layer' (specifically from 'Layer')
# Note that cocos is the name of the module, and we are accessing 'layer.Layer'
# of that module using the '.' operator.

class Window(cocos.layer.Layer):    

    # This is the contrustor of the Window class.
    # Every class has a constructor.
    # A constructor can have parameters, that can initialize the attributes of a class
    # For example: def __init__(self, name, age=22):
    # Make sure you include always, for all methods of a class, the special parameter
    # 'self' which basically referes to the object that you are manipulating.
    def __init__(self): # Note that __init__ is not a typo.

        # Calling the (super) constructor of cocos.layer.Layer
        # Initializing the part of this object that belongs to cocos.layer.Layer
        # Note that we are calling the __init__ of the 'super' class (cocos.layer.Layer)
        # Note that we pass 'Window', this class, and 'self',
        # which will refer to the current object of type 'Window' that you will create.
        super(Window, self).__init__()

        # 'self.label' is an attribute
        # Use self.name_of_attribute in this method __init__()
        # To define an attribute that a class has. You can define many attributes as you want.

        # This is an attribute, because 'label' is preceded by 'self'.
        # You use self to refer to everything that is part of this class (Window)
        # This attribute is an instance of the class 'text.Label' (specifically 'Label')
        # When you call 'Label(params)' you are actually calling the constructor,
        # the __init__(self) method, of the class 'Label'. In this case, the costructor of
        # 'Label' receives some parameters, as you can see: "Hello, world"...
        
        self.label = cocos.text.Label('Hello, world', font_name='Times New Roman', font_size=32, anchor_x='center',
                                      anchor_y='center')

        # Now that we have created self.label (which is of type 'Label'),
        # We want to modify the self.label position inside the screen.
        self.label.position = (320, 240)

        # Now that we have set up the appearance of the 'label',
        # we have to add it to the screen:
        self.add(self.label)
        
    # END OF CONSTRUCTOR
    
# END OF CLASS


# We have define the class that will represent our "canvas",
# Now we need actually to create and initialize the real window.
# In Cocos2D, we do it like this:
cocos.director.director.init() # Note that this is not inside the class!

# Now we can create our object of type Window, and we do it, remember,
# calling the constructor (the __init__) of the same class.
# That is done using this syntax: NameOfTheClass(eventual_parameters_that__init__receives)
win = Window()
# You want to create an object of type 'Window',
# and we want to store it in 'win',
# which is a 'normal' variable that holds the object of type 'Window' just created.

# Now we have to create a Scene object, which is stored in 'main_scene'.
# Note that we pass the object of type 'Window' that we have just created above
# to the initializer method __init__ of the class Scene:
# A 'Scene' object, needs a 'Window' object to be created.
main_scene = cocos.scene.Scene(win)

# Here we are just saying to the 'director' to run the 'main_scene'!
cocos.director.director.run(main_scene)
