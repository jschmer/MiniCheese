# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

from Move import Move

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

        self.load_board(str_rep)


    def load_board(self, str_rep):
        """
        The board is a list of list of pieces. The list is reversed and framed by # chars.
        """
        # strip newlines at beginning and end
        lines = str_rep.strip().split("\n")
        if len(lines) != 7:
            raise ValueError("Invalid board size")

        move_num, turn = lines[0].split(" ")
        self.move_num = int(move_num)
        self.turn = turn
        if self.turn not in Board.colors:
            raise ValueError("Invalid turn")

        self.board.append(["#"] * 7)

        for line in lines[1:]:
            line = line.strip()
            if len(line) != 5:
                raise ValueError("Invalid line size")

            for char in line:
                if char not in self.pieces:
                    raise ValueError("Invalid piece")

            self.board.append(list("#" + line + "#"))

        self.board.append(["#"] * 7)
        self.board.reverse()


    def move(self, move):
        assert isinstance(move, Move)
        # For now, no legality checks are done
        self.board[move.end.y][move.end.x] = self.board[move.start.y][move.start.x]
        self.board[move.start.y][move.start.x] = '.'
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
        result = []
        result.append("{} {}".format(self.move_num, self.turn))

        # leave out the # chars
        for line in reversed(self.board[1:-1]):
            result.append("".join(line[1:-1]))

        return "\n".join(result) + "\n"
