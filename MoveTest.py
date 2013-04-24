# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

import unittest 
from Move import Move

class MoveTest(unittest.TestCase):

    def test_construct(self): 
        b = Move((1, 1), (1, 2))
        self.assertEqual((1, 1), b.start)
        self.assertEqual((1, 2), b.end)

        b = Move.from_string("a1-a2")
        self.assertEqual((1, 1), b.start)
        self.assertEqual((1, 2), b.end)

    def test_to_str(self):
        b = Move((1, 1), (1, 2))
        self.assertEqual(str(b), "a1-a2")

        b = Move((1, 1), (5, 6))
        self.assertEqual(str(b), "a1-e6")

    def test_equal_operator(self):
        b = Move.from_string("a1-a2")
        c = Move.from_string("a1-a2")
        self.assertEqual(b, c)

        b = Move.from_string("e1-a2")
        c = Move.from_string("a1-a4")
        self.assertNotEqual(b, c)

if __name__ == "__main__": 
    unittest.main()