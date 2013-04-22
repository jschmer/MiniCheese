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
        with self.assertRaisesRegex(ValueError, "Wrong row/col index"):
            b = Position(0, 4)

    def test_construct_from_string(self):
        b = Position.from_string("b6")

        self.assertEqual(b.x, 2)
        self.assertEqual(b.y, 6)

    def test_construct_from_string_error(self):
        with self.assertRaisesRegex(ValueError, "Too much position information"):
            b = Position.from_string("z4a")

        with self.assertRaisesRegex(ValueError, "Wrong row index"):
            b = Position.from_string("a7")

        with self.assertRaisesRegex(ValueError, "Wrong column index"):
            b = Position.from_string("z4")

    def test_to_str(self):
        b = Position.from_string("a4")
        self.assertEqual(str(b), "a4")

        b = Position(1, 4)
        self.assertEqual(str(b), "a4")

    def test_equal_operator(self):
        b = Position.from_string("a4")
        c = Position(1, 4)
        self.assertEqual(b, c)

        b = Position.from_string("a4")
        c = Position(4, 4)
        self.assertNotEqual(b, c)

if __name__ == "__main__": 
    unittest.main()