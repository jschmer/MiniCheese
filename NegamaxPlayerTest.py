# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

import unittest
import random
from NegamaxPlayer import NegamaxPlayer
from Board import Board
from Move import Move

class NegamaxPlayerTest(unittest.TestCase):

    def test_negamax(self):
        board = Board("""
                        1 W
                        ..k..
                        .....
                        .....
                        .....
                        ..Q..
                        ...K.
                        """)

        player = NegamaxPlayer()
        best_value, best_move = player.negamax(board, 1)
        self.assertEqual(Move.from_string("c2-c6"), best_move)


        random.seed(0)
        board = Board("""
                        1 W
                        kp...
                        .p...
                        .....
                        .....
                        .Q...
                        ...K.
                        """)

        player = NegamaxPlayer()
        best_value, best_move = player.negamax(board, 3)
        self.assertEqual(Move.from_string("b2-b4"), best_move)


if __name__ == "__main__": 
    unittest.main()