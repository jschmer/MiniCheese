# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

from Move import Move
from Position import Position

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

    def _load_board(self, str_rep):
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

    def is_own_piece(self, c):
        if not c in Board.pieces:
            assert False

        if c.isupper():
            return self.turn == "W"
        elif c.islower():
            return self.turn == "B"
        else:
            assert False

    def is_within_bounds(self, pos):
        if pos.x < 1 or pos.y > 5:
            return False
        if pos.y < 1 or pos.y > 6:
            return False
        return True

    def piece_at(self, pos):
        return self.board[pos.y][pos.x]

    def scan(self, pos, dx, dy, only_capture = False, no_capture = False, one_step=False):
        """
        only_capture implies only one step
        """
        assert isinstance(pos, Position)
        newpos = Position(pos.x, pos.y)
        moves = []
        while True:
            try:
                newpos = Position(newpos.x + dx, newpos.y + dy)
            except ValueError:
                # out of bounds
                break

            piece = self.piece_at(newpos)
            if only_capture:
                # pawn bastard
                if piece == '.': break
                elif self.is_own_piece(piece): break
                else: 
                    moves.append(Move(pos, newpos))
                    break
            else:
                # everything else
                if piece == '.':
                    # legal move
                    moves.append(Move(pos, newpos))
                elif self.is_own_piece(piece):
                    # collision with own piece
                    break
                else:
                    if no_capture == False:
                        # capture enemy piece
                        moves.append(Move(pos, newpos))
                    break

            if one_step:
                break
        return moves

    def legal_moves(self):
        '''
        computes a list of legal moves for the current player and returns it
        '''
        for row in self.board:
            for field in row:
                if field in ['#', '.']:
                    pass


        return []

    def move(self, move):
        """The caller guarantees that the move is legal."""
        assert isinstance(move, Move)

        old_piece_end = self.board[move.end.y][move.end.x] 
        new_piece_end = self.board[move.start.y][move.start.x]

        # pawn promotion
        if new_piece_end == 'p' and move.end.y == 1:
            assert self.turn == 'B'
            new_piece_end = 'q'
        elif new_piece_end == 'P' and move.end.y == 6:
            assert self.turn == 'W'
            new_piece_end = 'Q'

        self.board[move.end.y][move.end.x] = new_piece_end
        self.board[move.start.y][move.start.x] = '.'

        if self.turn == "W":
            self.turn = "B"
        else:
            self.move_num += 1
            self.turn = "W"

        # king capture and result
        if old_piece_end == 'k':
            result = 'W'
        elif old_piece_end == 'K':
            result = 'B'
        elif self.move_num == 41:
            result = '='
        else:
            result = '?'
        return result


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
