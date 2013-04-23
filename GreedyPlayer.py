# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

from Board import Board
import copy

class GreedyPlayer(object):
    def generate_move(self, game):
        """
        Generate and return a move for the current turn color.
        The caller ensures that a legal move exists.
        Always takes the next best move for itself.
        """
        legal_moves = game.legal_moves()
        assert legal_moves

        scored_moves = []
        for move in legal_moves:
            board = copy.deepcopy(game)
            board.move(move)
            score = board.score()
            scored_moves.append((score, move))

        scored_moves = sorted(scored_moves, key=lambda t: t[0])
        return scored_moves[0][1]