"""
AUTHOR: Nelson Dos Santos
LECTURE 2 - More about classes. Actions.
TOPICS:
    1. Classes
    2. Objects
    3. ACTIONS: Scaling and Rotating!
    
COMMENT: If you don't understand something, you should ask me immediately,
and I will try to answer is the best way I can. This OOP paradigm will help be used
always the next semester, so if you learn it now, you will be more confortable.
If we don't finish the game, ok, but at least we are trying to learn something very useful!!

I hope you like to learn this, and don't hesitate, again, to ask me for help!!!

YOU SHOULD TRY TO IMPLEMENT WHAT IS IN THIS SCRIPT BY YOURSELF!!!!
"""

import cocos # NEVER FORGET TO IMPORT THE GOD MODULE


# Let's talk about actions, interesting, uhm?

# If you don't know what an action is, then think about it!
# If you have just thought about that, then you have finished an action ;)

# If you plan to have many actions in your program,
# then you should import all the actions. You do that using this syntax.

from cocos.actions import *


# Now, we create another class (You can give to it whatever name you prefer)
# Note that I am deriving 'ActionsClass' from 'cocos.layer.ColorLayer' specifically from  'ColorLayer'
class ActionsClass(cocos.layer.ColorLayer):


    # Constructor or initializer. Remember, every class has a constructor!
    def __init__(self):

        # Calling the constructor or initializer of the 'Mother' class (ColorLayer)
        # You use super, remember?
        # Note that the constructor of ColorLayer receives 4 parameters.
        # These parameters are probably the default values for the RGB model (plus the alpha value for transparency?) 
        super(ActionsClass, self).__init__(64, 64, 224, 255)

        # We create another label.
        # Remember, if you want to create an attribute for a class
        # You have to do it in the __init__ method (constructor) using the following syntax.
        # 'self.name_of_the_attribute = default_value'
        # Remember also that all functions of a class have as first parameter the 'self' keyword!!!
        self.label = cocos.text.Label("Keep working hard, dudes!", font_name="Times New Roman",
                                      font_size=32, anchor_x="center", anchor_y="center")
        
        # We have just created an attribute for this class ActionsClass,
        # now we can also modify the 'attributes' of this attribute. (Did you like the pun?)
        # Modifying the position again.
        self.label.position = (320, 240)

        # Adding self.label to ActionsClass class, which, remember, derives from ColorLayer
        self.add(self.label)
        
        # Let's create an new object of type Sprite (Can we drink it?)
        # MAKE SURE YOU HAVE AN IMAGE WITH THE NAME 'image.png'
        # WHERE THIS SCRIPT IS EXECUTED!!!
        self.sprite = cocos.sprite.Sprite('image.png')

        # Let's also modify the default values of our Sprite object called 'sprite'
        # Setting 'sprite' in the center of the screen
        self.sprite.position = (320, 240)

        # Setting the scale of 'sprite' to 3 (will increase 3 times). Default value is 1.
        self.sprite.scale = 1
    
        # Now, we can add our 'sprite' object to ActionsClass.
        # Second paramter specifies if we want to override the previous added objects (self.label)
        # In our case, yes, we want to cover it, that's why we set 'z' to 1 (instead of the default 0)
        self.add(self.sprite, z=1)

        # Now, since we want to deal with ACTIONS, we create a 'ScaleBy' action,
        # which basically, in the following case, scale 3 times the object in 2 seconds:

        scale = ScaleBy(3, duration=2) # BY THE WAY, HAVE YOU UNDERSTOOD THE PURPOSE OF THE KEYWORD self?

        # But we want to apply this action to which object?? The calm is the solution :)

        # Now, this is CoMpLiCaTeD, but keep working dudes!
        # We tell the 'self.label' to
            # 1. Scale 3 times in in 2 seconds
            # 2. then To scale back 3 times in 2 seconds (very useful)
            # and we repeat these 2 actions forever (which is too much!)

        # Notice that the + operator is the 'Sequence' action:
        # Calling the function 'do' of the object attribute 'self.label':
        self.label.do( Repeat(scale + Reverse(scale)) )
        # Difficult? Keep trying to understand it ;)
        # Now we tell the sprite to do the same thing,
        # but the 'sprite' starts the 'scale back' action!
        self.sprite.do( Repeat(Reverse(scale) + scale) )
        
    # END OF THE CONSTRUCTOR, a.k.a __init__, aka INITIALIZER
# END OF THE CLASS

# Now we need a director, right? But we need it initialized!
cocos.director.director.init()

# Creating an object of type ActionsClass
action_object = ActionsClass()

# And... we tell the Layer (action_object)
# (yes, all CocosNode objects can execute actions)
# to execute a RotateBy action of 360 degrees in 10 seconds (PLAGARISM)
action_object.do( RotateBy(360, duration=10) )


# FINALLYYY :D
# Guess what? We create the scene where to put our class of type ActionsClass,
# which derivee from a class of type ColorLayer.

main_scene = cocos.scene.Scene(action_object) # Passing our object to the __init__ of the class Scene.

# FOREST, RUN, BUT DON'T FORGET THE SCENE OTHERWISE YOU CAN FALL DOWN :D)
cocos.director.director.run(main_scene)

