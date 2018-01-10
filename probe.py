import os

class Probe:

    def __init__ (self, path):
        self._probe = open(path, 'w')
        self._activity = 0
        self._dbg = 0

    def output_activity (self):
        self._probe.write(str(self._activity) + "\t" + str(self._dbg) + "\n")
        self._activity = 0
        self._dbg = 0

    def dbg (self, val):
        self._dbg = val

    def read (self, activity):
        self._activity += activity
        
    def __del__ (self):
        self._probe.close()
