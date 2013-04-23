# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

from Board import Board
import copy
from random import choice

class GreedyPlayer(object):
    def generate_move(self, game):
        """
        Generate and return a move for the current turn color.
        The caller ensures that a legal move exists.
        Always takes the next best move for itself.
        """
        legal_moves = game.legal_moves()
        assert legal_moves

        # calculate a score for each move
        scored_moves = []
        for move in legal_moves:
            board = copy.deepcopy(game)
            board.move(move)
            score = board.score()
            scored_moves.append((score, move))

        # sort the moves on their score
        scored_moves = sorted(scored_moves, key=lambda t: t[0])

        # extract the best moves
        best_moves = []
        best_score = scored_moves[0][0]
        for scored_move in scored_moves:
            if scored_move[0] == best_score:
                best_moves.append(scored_move)
            else:
                break

        # pick a random move out of the best ones
        return choice(best_moves)[1]