# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

import unittest 
from Board import Board

class BoardTest(unittest.TestCase):

    def test_construct_default(self): 
        b = Board()

        self.assertEqual(b.board, [["k", "q", "b", "n", "r"],
                                   ["p", "p", "p", "p", "p"],
                                   [".", ".", ".", ".", "."],
                                   [".", ".", ".", ".", "."],
                                   ["P", "P", "P", "P", "P"],
                                   ["R", "N", "B", "Q", "K"]])
        self.assertEqual(b.move, 1)
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
        self.assertEqual(b.move, 11)
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



if __name__ == "__main__": 
    unittest.main()