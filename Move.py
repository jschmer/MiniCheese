# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

class Move(object):
    """description of class"""

    def __init__(self, fr, to):
        self.start = fr
        self.end   = to

    def __str__(self):
        return str(self.start) + " -> " + str(self.end)

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end


