# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

import unittest 
from Position import Position

class PositionTest(unittest.TestCase):

    def test_construct(self): 
        b = Position(3, 4)

        self.assertEqual(b.x, 3)
        self.assertEqual(b.y, 4)

    def test_construct_error(self): 
        with self.assertRaises(ValueError):
            b = Position(0, 4)

    def test_construct_from_string(self):
        b = Position.from_string("b6")

        self.assertEqual(b.x, 2)
        self.assertEqual(b.y, 6)

    def test_construct_from_string_error(self):
        with self.assertRaises(ValueError):
            b = Position.from_string("a7")

        with self.assertRaises(ValueError):
            b = Position.from_string("z4")

    def test_to_str(self):
        b = Position.from_string("a4")
        self.assertEqual(str(b), "a4")

        b = Position(1, 4)
        self.assertEqual(str(b), "a4")


if __name__ == "__main__": 
    unittest.main()