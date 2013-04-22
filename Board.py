# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

class Board(object):
    """Board representation of a MiniChess board.

    The bottom left piece has the coordinates a1 or 11.
    Top right has e6 or 56.
    """
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

        self._load_board(str_rep)

    def is_own_piece(self, c):
        if not c in Board.pieces:
            assert False

        if c.isupper():
            return self.turn == "W"
        elif c.islower():
            return self.turn == "B"
        else:
            assert False

    def scan(self, pos, dx, dy, one_step = False, only_capture = False):
        pass

    def legal_moves(self):
        '''
        computes a list of legal moves for the current player and returns it
        '''
        return []

    def _load_board(self, str_rep):
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
        self.board[6 - move.end.y][move.end.x - 1] = self.board[6 - move.start.y][move.start.x - 1]
        self.board[6 - move.start.y][move.start.x - 1] = '.'
        if self.turn == "W":
            self.turn = "B"
        else:
            self.move_num += 1
            self.turn = "W"

    def __eq__(self, other):
        return (self.move_num == other.move_num and
                self.turn == other.turn and
                self.board == other.board)

    def __str__(self):
        str = "{} {}\n".format(self.move_num, self.turn)
        str += "\n".join(["".join(line) for line in self.board])
        str += "\n"
        return str
