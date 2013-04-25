# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

import copy
import sys
from time import time
import random
from Board import Board
from random import choice
import Player

random.seed(0)

class IterativeDeepeningPlayer(Player.Player):
    def __init__(self):
        self.start_time = time()
        self.match_duration = 300

    def generate_move(self, game):
        """
        Generate and return a move for the current turn color.
        The caller ensures that a legal move exists.
        Takes a move based on a search down a few moves.
        """
        # time_left = duration - time_spent
        time_left = self.match_duration - (time() - self.start_time)

        # max_move_time = time_left / (41 - game.move_num)
        max_move_time = time_left / (41 - game.move_num)
        self.end_time = time() + max_move_time

        # negamax it!
        a = -500000
        b = -a

        depth = 2
        self.node_count = 0
        _, shallow_move = self.negamax(game, 1, a, b)
        while True:
            try:
                deeper_value, deeper_move = self.negamax(game, depth, a, b)
            except TimeoutError:
                # time expired

                # returns the shallow move
                break

            print("D:", depth, "-", "Value for", deeper_move, "=", deeper_value)

            # handle game end conditions
            if deeper_value >= 100000:
                # found win
                return deeper_move
            # TODO: handle draw!
            elif deeper_value <= -100000:
                # found draw or loss
                # return previous move which didn't find a loss or draw
                # which guarantees a loss in at least depth-1 moves
                return shallow_move

            shallow_move = deeper_move
            depth += 1

        return shallow_move

    def negamax(self, state, max_depth, alpha, beta):
        # base case
        if max_depth <= 0:
            return (state.score(), None)

        # check time
        if self.node_count % 10000 == 0:
            # update time left
            if time() > self.end_time:
                raise TimeoutError("Badäng!")

        self.node_count += 1

        # recursive case
        legal_moves = state.legal_moves()
        
        # pre sort the moves! best first!
        sorted_moves = []
        for move in legal_moves:
            score = state.score_after(move)
            sorted_moves.append((score, move))

        # sort the moves on their score
        sorted_moves = sorted(sorted_moves, key=lambda t: t[0])

        best_value = -sys.maxsize
         
        for value, move in sorted_moves:
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