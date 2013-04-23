# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

class Move(object):
    """description of a move"""
    cols = "abcde"
    rows = "123456"

    def __init__(self, fr, to):
        """
        fr and to are tuples in the form "(x, y)"
        """
        self.start = fr
        self.end   = to

    def __str__(self):
        return self.pos_to_str(self.start) + "-" + self.pos_to_str(self.end)

    def pos_to_str(self, pos):
        return Move.cols[pos[0]-1]+str(pos[1])

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def parse_position(msg):
        if len(msg) > 2: raise ValueError("Too much position information")
        if msg[0] not in Move.cols: raise ValueError("Wrong column index")
        if msg[1] not in Move.rows: raise ValueError("Wrong row index")

        x = Move.cols.index(msg[0])+1
        y = int(msg[1])
        return (x, y)

    def from_string(msg):
        msg = msg.strip()
        start, end = msg.split("-")

        return Move(Move.parse_position(start), Move.parse_position(end))