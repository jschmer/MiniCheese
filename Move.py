# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

from Position import Position

class Move(object):
    """description of class"""

    def __init__(self, fr, to):
        self.start = fr
        self.end   = to

    def __str__(self):
        return str(self.start) + "-" + str(self.end)

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def from_string(msg):
        start, end = msg.split("-")
        return Move(Position.from_string(start), Position.from_string(end))
