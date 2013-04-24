# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

import copy
import sys
import random
from Board import Board
from random import choice

random.seed(0)

class NegamaxPruningPlayer(object):
    def generate_move(self, game):
        """
        Generate and return a move for the current turn color.
        The caller ensures that a legal move exists.
        Takes a move based on a search down a few moves.
        """
        # negamax it!
        a = -500000
        b = -a
        value, move = self.negamax(game, 3, a, b)
        print("Value:", value)
        return move

    def negamax(self, state, max_depth, alpha, beta):
        # base case
        if max_depth <= 0:
            return (state.score(), None)

        # recursive case
        legal_moves = state.legal_moves()
        best_value = -sys.maxsize
        
        for move in legal_moves:
            newstate = Board.from_other(state)
            result = newstate.move(move)
            if result in ('W','B'):
                value = -newstate.score()
            elif result == '=':
                value = 0
            else:
                value = -self.negamax(newstate, max_depth-1, -beta, -alpha)[0]

            if value > beta:
                return (value, None)
            if value > alpha:
                alpha = value

            if value > best_value:
                best_value = value
                best_move = move
            elif value == best_value:
                if random.choice((True,False)):
                    best_value = value
                    best_move = move
        return (best_value, best_move)