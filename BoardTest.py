# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

import unittest 
from Board import Board

class BoardTest(unittest.TestCase):

    def est_construct_default(self): 
        b = Board()

        self.assertEqual(b.board, ["kqbnr",
                                   "ppppp",
                                   ".....",
                                   ".....",
                                   "PPPPP",
                                   "RNBQK"])
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
        self.assertEqual(b.board, ["..bn.",
                                   "pp...",
                                   ".....",
                                   "PP...",
                                   "..PPP",
                                   "RNBQK"])
        self.assertEqual(b.move, 11)
        self.assertEqual(b.turn, "B")

    def test_construct_from_string_error(self):
        self.assertRaises(ValueError, Board("""
            11 Z
            ..bn.
            pp...
            .....
            PP...
            ..PPP
            RNBQK
            """))

if __name__ == "__main__": 
    unittest.main()