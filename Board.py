# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

class Board(object):
    """Board representation of a MiniChess board"""
    colors = "BW"
    pieces = "kqbnrpKQBNRP."

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
        # strip newlines at beginning and end
        lines = str_rep.strip().split("\n")
        if len(lines) != 7:
            raise ValueError("Invalid board size")

        move, turn = lines[0].split(" ")
        self.move = int(move)
        self.turn = turn
        if self.turn not in Board.colors:
            raise ValueError("Invalid turn")

        for line in lines[1:]:
            line = line.strip()
            if len(line) != 5:
                raise ValueError("Invalid line size")

            for char in line:
                if char not in self.pieces:
                    raise ValueError("Invalid piece")

            self.board.append(list(line))

    def __str__(self):
        str = "{} {}\n".format(self.move, self.turn)
        str += "\n".join(["".join(line) for line in self.board])
        str += "\n"
        return str
