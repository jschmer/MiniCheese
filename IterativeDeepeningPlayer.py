# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

import copy
import sys
from time import time
import random
from Board import Board
from random import choice
import Player


class TimeUpError(Exception):
    pass


class IterativeDeepeningPlayer(Player.Player):
    def __init__(self):
        self.match_duration = 295
        self.time_spent = 0

    def generate_move(self, game):
        """
        Generate and return a move for the current turn color.
        The caller ensures that a legal move exists.
        Takes a move based on a search down a few moves.
        """

        move_start_time = time()

        # time_left = duration - time_spent
        time_left = self.match_duration - self.time_spent

        # max_move_time = time_left / (41 - game.move_num)
        max_move_time = time_left / (41 - game.move_num + 1)
        self.end_time = time() + max_move_time - 0.5
        print("time_left:", time_left)
        print("max_move_time:", max_move_time)


        # negamax could end up corrupting the board so
        # copy the game board for every negamax iteration
        game_copy = Board.from_other(game)

        # alpha-beta values
        a = -500000
        b = -a

        depth = 2
        self.node_count = 0
        shallow_value, shallow_move = self.negamax(game_copy, 1, a, b)
        while True:
            # negamax could end up corrupting the board so
            # copy the game board for every negamax iteration
            game_copy = Board.from_other(game)
            try:
                deeper_value, deeper_move = self.negamax(game_copy, depth, a, b)
            except TimeUpError:
                # time expired
                # returns the shallow move
                break
            if not depth > 20:
                print("D:", depth, "-", "Value for", deeper_move, "=", deeper_value)

            # handle game end conditions
            if deeper_value >= 100000:
                # found win
                print("found win")
                shallow_move = deeper_move
                break

            # TODO: handle draw!
            elif deeper_value <= -100000:
                print("found loss")
                # found draw or loss
                # return previous move which didn't find a loss or draw
                # which guarantees a loss in at least depth-1 moves
                # returns shallow_move
                break

            shallow_move = deeper_move
            shallow_value = deeper_value
            depth += 1

        self.time_spent += time() - move_start_time
        return shallow_move

    def negamax(self, state, max_depth, alpha, beta):
        # base case
        if max_depth <= 0:
            return (state.score(), None)

        # check time
        if self.node_count % 1000 == 0:
            # update time left
            if time() > self.end_time:
                raise TimeUpError()

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
            result = state.move(move)
            if result in ('W','B'):
                value = -state.score()
            elif result == '=':
                value = 0
            else:
                value = -self.negamax(state, max_depth-1, -beta, -alpha)[0]

            state.undo_last_move()

            if value >= beta:
                return (value, move)
            if value > alpha:
                alpha = value

            if value > best_value:
                best_value = value
                best_move = move
            elif value == best_value:
                pass
        return (best_value, best_move)