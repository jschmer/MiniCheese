# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

class Board(object):
    """Board representation of a MiniChess board"""
    colors = "BW"
    pieces = "kqbnrpKQBNRP."

    def __init__(self, str_rep = None):
        self.board = []
        self.move_num = 1
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

        move_num, turn = lines[0].split(" ")
        self.move_num = int(move_num)
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

    def move(self, move):
        # For now, no legality checks are done
        self.board[move.end.y-1][move.end.x-1] = self.board[move.start.y-1][move.start.x-1]
        self.board[move.start.y-1][move.start.x-1] = '.'
        self.move_num += 1
        self.turn = "W" if self.turn == "B" else "B"


    def __str__(self):
        str = "{} {}\n".format(self.move_num, self.turn)
        str += "\n".join(["".join(line) for line in self.board])
        str += "\n"
        return str
