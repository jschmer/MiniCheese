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
        'k': -100000,
        'q': -700,
        'b': -300,
        'n': -250,
        'r': -500,
        'p': -125,
        'K': 100000,
        'Q': 700,
        'B': 300,
        'N': 250,
        'R': 500,
        'P': 125,
        '.': 0
    }

    def __init__(self, str_rep = None):
        self.board = []
        self.move_num = 1
        self.turn = "W"
        self.history = []

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

        self.cur_score = self._calc_score()

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
        for y in range(1, 7):
            for x in range(1, 6):
                yield (x, y)

    def fields(self):
        for y in range(1, 7):
            for x in range(1, 6):
                yield self.board[y-1][x-1] 

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
        newpos = pos

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

    def _bonus_score(self, pos, piece):
        """calculates a bonus score for the piece on pos"""
        # from whites pov
        # white pieces get positive bonus
        # black ones negative

        if piece == '.': return 0

        whites_piece = piece.isupper()
        if whites_piece:
            # how far is this piece from its baseline?
            distance = pos[1] - 1
        else:
            distance = 6 - pos[1]

        bonus = 0
        p = piece.lower()
        if p == 'p':
            # pawn
            bonus = distance * 20
        else:
            # everything except king
            if distance > 0:
                bonus = 10

        if whites_piece: return bonus
        else: return -bonus


    def move(self, move):
        """
        The caller guarantees that the move is legal.
        The score is calculated 'on the move'
        """
        assert isinstance(move, Move)

        old_piece_end = self.at(move.end)
        new_piece_end = piece_start = self.at(move.start)
        new_score = self.cur_score

        # pawn promotion
        if new_piece_end == 'p' and move.end[1] == 1:
            assert self.turn == 'B'
            new_piece_end = 'q'
            new_score -= Board.piece_values['p']
            new_score += Board.piece_values['q']
        elif new_piece_end == 'P' and move.end[1] == 6:
            assert self.turn == 'W'
            new_piece_end = 'Q'
            new_score -= Board.piece_values['P']
            new_score += Board.piece_values['Q']

        new_score -= Board.piece_values[old_piece_end]
        self.set(move.end, new_piece_end)
        self.set(move.start, '.')

        # remove bonus score of start piece
        new_score -= self._bonus_score(move.start, piece_start)

        # remove bonus score of captured piece
        new_score -= self._bonus_score(move.end, old_piece_end)

        # add bonus score of end piece
        new_score += self._bonus_score(move.end, new_piece_end)

        if self.turn == "W":
            self.turn = "B"
        else:
            self.move_num += 1
            self.turn = "W"

        # king capture and result
        if old_piece_end == 'k':
            result = 'W'
            new_score = 100000
        elif old_piece_end == 'K':
            result = 'B'
            new_score = -100000
        elif self.move_num == 41:
            result = '='
            new_score = 0
        else:
            result = '?'

        # save old state to be able to undo it later
        # ((startpos, startpiece), (endpos, endpiece), score)
        # if self._calc_score() != new_score:
        #     print("calc_score:", self._calc_score(), "new_score:")
        #     print("Wtf")
        self.history.append(((move.start, piece_start), (move.end, old_piece_end), self.cur_score))

        self.cur_score = new_score
        return result
   
    def undo_last_move(self):
        """Undos the last move in the history. Returns nothing."""

        # change turn and move_num
        if self.turn == "W":
            self.move_num -= 1
            self.turn = "B"
        else:
            self.turn = "W"

        assert self.history
        last_move = self.history.pop()
        # ((startpos, startpiece), (endpos, endpiece), score)
        self.set(last_move[0][0], last_move[0][1])
        self.set(last_move[1][0], last_move[1][1])
        self.cur_score = last_move[2]


    def score_after(self, move):
        """
        The caller guarantees that the move is legal.
        This function just calculates the score after the given move,
        without actually altering the board.
        It's blazingly fast! :D
        """
        assert isinstance(move, Move)

        score = self.cur_score
        turn = self.turn
        move_num = self.move_num

        old_piece_end = self.at(move.end)
        new_piece_end = piece_start = self.at(move.start)

        # pawn promotion
        if new_piece_end == 'p' and move.end[1] == 1:
            assert self.turn == 'B'
            new_piece_end = 'q'
            score -= Board.piece_values['p']
            score += Board.piece_values['q']
        elif new_piece_end == 'P' and move.end[1] == 6:
            assert self.turn == 'W'
            new_piece_end = 'Q'
            score -= Board.piece_values['P']
            score += Board.piece_values['Q']

        score -= Board.piece_values[old_piece_end]

        # remove bonus score of start piece
        score -= self._bonus_score(move.start, piece_start)

        # remove bonus score of captured piece
        score -= self._bonus_score(move.end, old_piece_end)

        # add bonus score of end piece
        score += self._bonus_score(move.end, new_piece_end)


        if turn == "W":
            turn = "B"
        else:
            move_num += 1
            turn = "W"

        # king capture and result
        if old_piece_end == 'k':
            score = 100000
        elif old_piece_end == 'K':
            score = -100000
        if move_num == 41:
            score = 0

        return score if turn == "W" else -score

    def _calc_score(self):
        """Calculates the score of the whole board from the view of whites turn"""
        score = 0
        black_king_found = False
        white_king_found = False
        for pos in self.positions():
            piece = self.at(pos)
            if piece == 'k':
                black_king_found = True
            elif piece == 'K':
                white_king_found = True
            score += Board.piece_values[piece]
            score += self._bonus_score(pos, piece)

        if not black_king_found:
            score = 100000
        if not white_king_found:
            score = -100000
        if self.move_num == 41:
            score = 0

        return score


    def score(self):
        """The score is positive if the current turn color has the better pieces."""
        # self.cur_score is the score for white, negate for black!
        return self.cur_score if self.turn == "W" else -self.cur_score

    def from_other(other_board):
        """Returns a copy of other_board."""
        new_board = Board.__new__(Board)
        new_board.turn = other_board.turn
        new_board.move_num = other_board.move_num
        new_board.cur_score = other_board.cur_score
        # history contents are immutable
        new_board.history = other_board.history[:]
        new_board.board = [line[:] for line in other_board.board]
        return new_board

    def __eq__(self, other):
        # we don't check the history
        return (self.move_num == other.move_num and
                self.turn == other.turn and
                self.board == other.board and
                self.cur_score == other.cur_score)

    def __str__(self):
        result = []
        result.append("{} {}".format(self.move_num, self.turn))

        for line in reversed(self.board):
            result.append("".join(line))

        return "\n".join(result)