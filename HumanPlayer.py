# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard
from Move import Move

class HumanPlayer(object):
    def generate_move(self, game):
        """
        Generate and return a move for the current turn color.
        The caller ensures that a legal move exists.
        If server checks if the move was legal and calls the function again if not.
        """
        a = input("Your move: ").strip()
        move = Move.from_string(a)
        return move