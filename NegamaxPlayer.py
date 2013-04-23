# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

import copy
import sys
from Board import Board
from random import choice

class NegamaxPlayer(object):
    def generate_move(self, game):
        """
        Generate and return a move for the current turn color.
        The caller ensures that a legal move exists.
        Takes a move based on a search down a few moves.
        """
        # negamax it!
        move = self.negamax(game, 4, True)
        return move

    def negamax(self, state, max_depth, return_move = False):
        """
        State has some legal moves left!
        """
        # base case
        if max_depth <= 0:
            return state.score()

        # recursive case
        legal_moves = state.legal_moves()
        best_value = -sys.maxsize
        
        for move in legal_moves:
            newstate = copy.deepcopy(state)
            result = newstate.move(move)
            if result in ('W','B','='):
                value = -newstate.score()
            else:
                value = -self.negamax(newstate, max_depth-1)

            if value > best_value:
                best_value = value
                best_move = move
        if return_move:
            return best_move
        else:
            return best_value