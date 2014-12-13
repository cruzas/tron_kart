"""
This file contains the tron timer class.
"""


class TTimer:
    """This class should only be used for this project.
    It simulates a Timer that has to be used inside a while or for loop.
    The class uses a counter variable as time counter."""
    def __init__(self, MAX):
        """MAX represents the TronTimer 'time' that a TronTimer object has to 'wait'."""
        self.max = MAX
        self.t = 0
        self.started = False
        self.finished = False
    #
    
    def start(self):
        """ WRITE HERE THE DOCS FOR THIS FUNCTION!!! """
        self.stop()
        self.started = True        
    #
    
    def inc(self):
        """ WRITE HERE THE DOCS FOR THIS FUNCTION!!! """
        if self.started:
            if self.t >= self.max:
                self.finished = True
            else:
                self.t += 1

    def ringing(self):
        """ WRITE HERE THE DOCS FOR THIS FUNCTION!!! """
        return self.finished
    #
    
    def stop(self):
        """ WRITE HERE THE DOCS FOR THIS FUNCTION!!! """
        self.started = False
        self.finished = False
        self.t = 0
    #
    
# end TronTimer
