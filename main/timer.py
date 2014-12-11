"""
Class 'Timer' simulates a timer that runs under a while or for loop.
The class was created specifically as a support class for the other classes
under this project, and you should NOT use it for other purposes,
if you do NOT know what is going on!
"""


class Timer:
    """ Using a counter varible,
this function simulates a timer under a while and for loop"""
    def __init__(self, MAX):
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

    def stopped(self):
        return self.finished

    def stop(self):
        self.started = False
        self.finished = False
        self.t = 0

