# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard
from Move import Move
from random import choice

class RandomPlayer(object):
    def generate_move(self, game):
        """
        Generate and return a move for the current turn color.
        The caller ensures that a legal move exists.
        """
        legal_moves = game.legal_moves()
        assert legal_moves
        return choice(legal_moves)