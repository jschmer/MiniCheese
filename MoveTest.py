# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

import unittest 
from Position import Position
from Move import Move

class MoveTest(unittest.TestCase):

    def test_construct(self): 
        p1 = Position.from_string("a1")
        p2 = Position.from_string("a2")
        b = Move(p1, p2)
        self.assertEqual(p1, b.start)
        self.assertEqual(p2, b.end)

    def test_to_str(self):
        p1 = Position.from_string("a1")
        p2 = Position.from_string("a2")
        b = Move(p1, p2)

        self.assertEqual(str(b), "a1 -> a2")

if __name__ == "__main__": 
    unittest.main()