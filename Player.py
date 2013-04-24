# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard
from Move import Move
from random import choice
import sys

class Player(object):
    def generate_move(self, game):
        pass
    def process_opponent_move(self, move):
        pass
    def process_result(self, result):
        pass


class HumanPlayer(Player):
    def generate_move(self, game):
        """
        Generate and return a move for the current turn color.
        The caller ensures that a legal move exists.
        If server checks if the move was legal and calls the function again if not.
        """
        a = input("Your move: ").strip()
        move = Move.from_string(a)
        return move


class RandomPlayer(Player):
    def generate_move(self, game):
        """
        Generate and return a move for the current turn color.
        The caller ensures that a legal move exists.
        """
        legal_moves = game.legal_moves()
        assert legal_moves
        return choice(legal_moves)


class SkirmishPlayer(Player):
    def generate_move(self, game):
        print("getting move from skirmish:")
        move = sys.stdin.readline()
        _, move = move.strip().split(" ")
        return Move.from_string(move)

    def process_opponent_move(self, move):
        print("informing skirmish of our move:")
        sys.stdout.write("! {}\r\n".format(move))
        sys.stdout.flush()

    def process_result(self, result):
        message = None
        if result == 'W':
            message = "= W wins"
        elif result == 'B':
            message = "= B wins"
        elif result == '=':
            message = "= Draw"

        if message:
            print("informing skirmish of our result:")
            sys.stdout.write(message + "\r\n")
            sys.stdout.flush()