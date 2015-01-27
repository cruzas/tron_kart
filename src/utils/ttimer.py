"""
Authors: Tron Team
Creation: December, 2014
Last update: 27.01.2015
Description: TTimer is an utility class for timing certain events
in the Tron Kart game
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
    
    def start(self):
        self.stop()
        self.started = True        
    
    def inc(self):
        if self.started:
            if self.t >= self.max:
                self.finished = True
            else:
                self.t += 1

    def ringing(self):
        return self.finished
    
    def stop(self):
        self.started = False
        self.finished = False
        self.t = 0
