# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

from Move import Move
from ScanArguments import scan_arguments as moves_for

class Board(object):
    """Board representation of a MiniChess board.

    The bottom left piece has the coordinates a1 or 11.
    Top right has e6 or 56.
    """
    colors = "BW"
    pieces = "kqbnrpKQBNRP."
    piece_values = {
        'q': -900,
        'b': -300,
        'n': -300,
        'r': -500,
        'p': -100,
        'Q': 900,
        'B': 300,
        'N': 300,
        'R': 500,
        'P': 100,
        '.': 0,
        '#': 0
    }

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

        for line in lines[1:]:
            line = line.strip()
            if len(line) != 5:
                raise ValueError("Invalid line size")

            for char in line:
                if char not in self.pieces:
                    raise ValueError("Invalid piece")

            self.board.append(list(line))

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
        """
        tests wheter the tuple pos (x, y) is within boards bounds
        (1,1) to (5,6)
        """
        if pos[0] < 1 or pos[0] > 5:
            return False
        if pos[1] < 1 or pos[1] > 6:
            return False
        return True

    def positions(self):
        for x in range(1, 6):
            for y in range(1, 7):
                yield (x, y)

    def at(self, pos):
        """
        pos is a tuple with x and y values
        (x, y)
        caller has to make sure that pos is within bounds!
        """
        return self.board[pos[1]-1][pos[0]-1] 

    def set(self, pos, piece):
        """
        pos is a tuple with x and y values
        (x, y)
        """
        if not self.is_within_bounds(pos):
            raise ValueError("Out of bounds!")
        if piece in Board.pieces:
            self.board[pos[1]-1][pos[0]-1] = piece

    def scan(self, move_list, pos, dx, dy, only_capture = False, no_capture = False, one_step=False):
        """
        only_capture implies only one step
        """
        assert isinstance(pos, tuple)
        newpos = (pos[0], pos[1])

        while True:
            newpos = (newpos[0] + dx, newpos[1] + dy)
            if not self.is_within_bounds(newpos):
                break

            piece = self.at(newpos)
            if only_capture:
                # pawn bastard
                if piece == '.': break
                elif self.is_own_piece(piece): break
                else: 
                    move_list.append(Move(pos, newpos))
                    break
            else:
                # everything else
                if piece == '.':
                    # legal move
                    move_list.append(Move(pos, newpos))
                elif self.is_own_piece(piece):
                    # collision with own piece
                    break
                else:
                    if no_capture == False:
                        # capture enemy piece
                        move_list.append(Move(pos, newpos))
                    break

            if one_step:
                break

    def legal_moves(self):
        '''
        computes a list of legal moves for the current player and returns it
        '''
        legal_moves = []
        for row in range(1, 7):
            for col in range(1, 6):
                position = (col, row)
                field = self.at(position)
                if not field in ['#', '.'] and self.is_own_piece(field):
                    possible_piece_moves = moves_for[field]
                    for move in possible_piece_moves:
                        self.scan(legal_moves, position, *move)

        return legal_moves

    def move(self, move):
        """The caller guarantees that the move is legal."""
        assert isinstance(move, Move)

        old_piece_end = self.at(move.end)
        new_piece_end = self.at(move.start)

        # pawn promotion
        if new_piece_end == 'p' and move.end[1] == 1:
            assert self.turn == 'B'
            new_piece_end = 'q'
        elif new_piece_end == 'P' and move.end[1] == 6:
            assert self.turn == 'W'
            new_piece_end = 'Q'

        self.set(move.end, new_piece_end)
        self.set(move.start, '.')

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

    def score(self):
        """The score is positive if the current turn color has the better pieces."""
        score = 0
        # this is written as if the current turn is white
        black_king_found = False
        white_king_found = False

        for position in self.positions():
            piece = self.at(position)
            if piece == 'k':
                black_king_found = True
            elif piece == 'K':
                white_king_found = True
            else:
                score += Board.piece_values[piece]

        if not black_king_found:
            score += 100000
        if not white_king_found:
            score -= 100000

        # now check if the turn is actually white
        return score if self.turn == "W" else -score

    def from_other(other_board):
        """Returns a copy of other_board."""
        new_board = Board.__new__(Board)
        new_board.turn = other_board.turn
        new_board.move_num = other_board.move_num
        new_board.board = [line[:] for line in other_board.board]
        return new_board

    def __eq__(self, other):
        return (self.move_num == other.move_num and
                self.turn == other.turn and
                self.board == other.board)

    def __str__(self):
        result = []
        result.append("{} {}".format(self.move_num, self.turn))

        for line in reversed(self.board):
            result.append("".join(line))

        return "\n".join(result)