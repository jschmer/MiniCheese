# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

class Board(object):
    """Board representation of a MiniChess board"""
    colors = "BW"
    pieces = "kqbnrpKQBNRP"

    def __init__(self, str_rep = None):
        self.board = []
        self.move = 1
        self.turn = "W"

        if str_rep == None:
            # load default board
            str_rep = """
            1 W
            kqbnr
            ppppp
            .....
            .....
            PPPPP
            RNBQK
            """

        self.load_board(str_rep)

    def load_board(self, str_rep):
        lines = str_rep.split("\n")
        move, turn = line[0].split(" ")
        self.move = int(move)
        self.turn = turn

        for line in lines[1:]:
            line = line.trim()
            # TODO sanity check
            self.board.append(line)

    def __str__(self):
        str = "{} {}\n".format(self.move, self.turn)
        str += "\n".join(self.board)
        return str

print("Board")