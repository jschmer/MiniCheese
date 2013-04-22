# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

import unittest 
from Board import Board
from Move import Move
from Position import Position

class BoardTest(unittest.TestCase):

    def test_construct_default(self): 
        b = Board()

        self.assertEqual(b.board, [["k", "q", "b", "n", "r"],
                                   ["p", "p", "p", "p", "p"],
                                   [".", ".", ".", ".", "."],
                                   [".", ".", ".", ".", "."],
                                   ["P", "P", "P", "P", "P"],
                                   ["R", "N", "B", "Q", "K"]])
        self.assertEqual(b.move_num, 1)
        self.assertEqual(b.turn, "W")

    def test_construct_from_string(self):
        b = Board("""
            11 B
            ..bn.
            pp...
            .....
            PP...
            ..PPP
            RNBQK
            """)
        self.assertEqual(b.board, [[".", ".", "b", "n", "."],
                                   ["p", "p", ".", ".", "."],
                                   [".", ".", ".", ".", "."],
                                   ["P", "P", ".", ".", "."],
                                   [".", ".", "P", "P", "P"],
                                   ["R", "N", "B", "Q", "K"]])
        self.assertEqual(b.move_num, 11)
        self.assertEqual(b.turn, "B")

    def test_construct_from_string_error(self):
        with self.assertRaises(ValueError):
            b = Board("""
                11 Z
                ..bn.
                pp...
                .....
                PP...
                ..PPP
                RNBQK
                """)

        with self.assertRaises(ValueError):
            b = Board("""
                 W
                ..bn.
                pp...
                .....
                PP...
                ..PPP
                RNBQK
                """)

        with self.assertRaises(ValueError):
            b = Board("""
                11 W
                ..bn.
                pp...
                .....
                PP...
                ..PPP
                RNBQK
                RNBQK
                """)

        with self.assertRaises(ValueError):
            b = Board("""
                11 W
                ..bn.
                pp...
                .....
                PP...
                ..PPP
                RNBQX
                """)

    def test_string_representation(self):
        b = Board()
        self.assertEqual(str(b), "1 W\nkqbnr\nppppp\n.....\n.....\nPPPPP\nRNBQK\n")

    def test_move(self):
        b = Board("""
            1 W
            kqbnr
            ppppp
            .....
            .....
            PPPPP
            RNBQK
            """)
        move = Move(Position(1,2), Position(1,3))
        b.move(move)
        self.assertEqual(str(b), "2 B\nkqbnr\n.pppp\np....\n.....\nPPPPP\nRNBQK\n")

        move = Move(Position(1,2), Position(1,3))
        b.move(move)
        self.assertEqual(str(b), "3 W\nkqbnr\n.pppp\n.....\n.....\nPPPPP\nRNBQK\n")

if __name__ == "__main__": 
    unittest.main()