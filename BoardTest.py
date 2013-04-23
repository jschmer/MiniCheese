# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

import unittest 
from Board import Board
from Move import Move
from Position import Position

class BoardTest(unittest.TestCase):

    def test_construct_default(self): 
        b = Board()

        self.assertEqual(b.board, [list("#######"),
                                   list("#RNBQK#"),
                                   list("#PPPPP#"),
                                   list("#.....#"),
                                   list("#.....#"),
                                   list("#ppppp#"),
                                   list("#kqbnr#"),
                                   list("#######")])
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
        self.assertEqual(b.board, [list("#######"),
                                   list("#RNBQK#"),
                                   list("#..PPP#"),
                                   list("#PP...#"),
                                   list("#.....#"),
                                   list("#pp...#"),
                                   list("#..bn.#"),
                                   list("#######")])
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
        b2 = Board("""
            1 B
            kqbnr
            ppppp
            .....
            P....
            .PPPP
            RNBQK
            """)

        self.assertEqual(b, b2)

        move = Move(Position(1,2), Position(1,3))
        b.move(move)
        b3 = Board("""
            2 W
            kqbnr
            ppppp
            .....
            .....
            .PPPP
            RNBQK
            """)
        self.assertEqual(b, b3)

    def test_move_promotion(self):
        b1 = Board("""
            1 W
            .....
            P....
            .....
            .....
            .....
            .....
            """)
        b1.move(Move.from_string("a5-a6"))
        b2 = Board("""
            1 B
            Q....
            .....
            .....
            .....
            .....
            .....
            """)
        self.assertEqual(b1, b2)

        b3 = Board("""
            1 B
            .....
            .....
            .....
            .....
            ..p..
            ...K.
            """)
        b3.move(Move.from_string("c2-d1"))
        b4 = Board("""
            2 W
            .....
            .....
            .....
            .....
            .....
            ...q.
            """)
        self.assertEqual(b3, b4)

    def test_move_game_result(self):
        # white win
        b = Board("""
            1 W
            .k...
            P....
            .....
            .....
            .....
            .....
            """)
        result = b.move(Move.from_string("a5-b6"))
        self.assertEqual(result, 'W')

        # black win
        b = Board("""
            1 B
            ..r..
            .....
            .....
            .....
            ..K..
            .....
            """)
        result = b.move(Move.from_string("c6-c2"))
        self.assertEqual(result, 'B')

        # undecided
        b = Board("""
            1 W
            .....
            P....
            .....
            .....
            .....
            .....
            """)
        result = b.move(Move.from_string("a5-a6"))
        self.assertEqual(result, '?')

        # draw
        b = Board("""
            40 B
            .....
            p....
            .....
            .....
            .....
            .....
            """)
        result = b.move(Move.from_string("a5-a4"))
        self.assertEqual(result, '=')



    def test_equality(self):
        b = Board()
        b2 = Board()
        self.assertTrue(b == b2)

        b3 = Board("""
            2 W
            kqbnr
            ppppp
            .....
            .....
            PPPPP
            RNBQK
            """)
        self.assertFalse(b == b3)

    def test_is_own_piece(self):
        b = Board()
        
        # whites turn
        self.assertTrue(b.is_own_piece('P'))
        self.assertFalse(b.is_own_piece('p'))

        b.move(Move.from_string("a1-a2"))

        # blacks turn
        self.assertFalse(b.is_own_piece('P'))
        self.assertTrue(b.is_own_piece('p'))

    def test_load_from_file(self):
        a = Board("""
                11 W
                ..bn.
                pp...
                .....
                PP...
                ..PPP
                RNBQK
                """)
        b = Board()
        with open("board_tests/dbg1.txt") as file:
            b = Board(file.read())
            self.assertEqual(a, b)

    def test_scan_until_bounds(self):
        b = Board("""
                    1 W
                    .....
                    .....
                    ..Q..
                    .....
                    .....
                    .....
                    """)
        startpos = Position(3,4)
        
        # to the right
        movelist = b.scan(startpos, 1, 0)
        expected = []
        expected.append(Move.from_string("c4-d4"))
        expected.append(Move.from_string("c4-e4"))
        self.assertEqual(expected, movelist)

        # to the left
        movelist = b.scan(startpos, -1, 0)
        expected = []
        expected.append(Move.from_string("c4-b4"))
        expected.append(Move.from_string("c4-a4"))
        self.assertEqual(expected, movelist)

        # to the top
        movelist = b.scan(startpos, 0, 1)
        expected = []
        expected.append(Move.from_string("c4-c5"))
        expected.append(Move.from_string("c4-c6"))
        self.assertEqual(expected, movelist)

        # to the bottom
        movelist = b.scan(startpos, 0, -1)
        expected = []
        expected.append(Move.from_string("c4-c3"))
        expected.append(Move.from_string("c4-c2"))
        expected.append(Move.from_string("c4-c1"))
        self.assertEqual(expected, movelist)

        # diagonal left top
        movelist = b.scan(startpos, -1, 1)
        expected = []
        expected.append(Move.from_string("c4-b5"))
        expected.append(Move.from_string("c4-a6"))
        self.assertEqual(expected, movelist)

        # diagonal right top
        movelist = b.scan(startpos, 1, 1)
        expected = []
        expected.append(Move.from_string("c4-d5"))
        expected.append(Move.from_string("c4-e6"))
        self.assertEqual(expected, movelist)

        # diagonal right bottom
        movelist = b.scan(startpos, 1, -1)
        expected = []
        expected.append(Move.from_string("c4-d3"))
        expected.append(Move.from_string("c4-e2"))
        self.assertEqual(expected, movelist)

        # diagonal left bottom
        movelist = b.scan(startpos, -1, -1)
        expected = []
        expected.append(Move.from_string("c4-b3"))
        expected.append(Move.from_string("c4-a2"))
        self.assertEqual(expected, movelist)

    def test_scan_until_own(self):
        b = Board("""
                    1 W
                    ....Q
                    .....
                    ..Q..
                    .....
                    .....
                    .....
                    """)
        startpos = Position(3,4)
        
        movelist = b.scan(startpos, 1, 1)
        expected = []
        expected.append(Move.from_string("c4-d5"))
        self.assertEqual(expected, movelist)

    def test_scan_until_enemy(self):
        b = Board("""
                    1 W
                    .....
                    .....
                    .....
                    ..q..
                    .....
                    Q....
                    """)
        startpos = Position(1,1)
        
        movelist = b.scan(startpos, 1, 1)
        expected = []
        expected.append(Move.from_string("a1-b2"))
        expected.append(Move.from_string("a1-c3"))
        self.assertEqual(expected, movelist)

    def test_scan_one_step(self):
        b = Board("""
                    1 W
                    .....
                    .....
                    .....
                    .Kq..
                    .....
                    .....
                    """)
        startpos = Position(2,3)
        
        # capturing right
        movelist = b.scan(startpos, 1, 0, one_step=True)
        expected = []
        expected.append(Move.from_string("b3-c3"))
        self.assertEqual(expected, movelist)

        # to the top
        movelist = b.scan(startpos, 0, 1, one_step=True)
        expected = []
        expected.append(Move.from_string("b3-b4"))
        self.assertEqual(expected, movelist)

    def test_scan_only_capture(self):
        b = Board("""
                    1 W
                    .....
                    ...p.
                    ..P..
                    ..K..
                    .....
                    .....
                    """)
        startpos = Position(3,4)
        
        # to the top
        movelist = b.scan(startpos, 0, 1, only_capture=True)
        expected = []
        self.assertEqual(expected, movelist)

        # capturing enemy
        movelist = b.scan(startpos, 1, 1, only_capture=True)
        expected = []
        expected.append(Move.from_string("c4-d5"))
        self.assertEqual(expected, movelist)

        # not capturing own
        movelist = b.scan(startpos, 0, -1, only_capture=True)
        expected = []
        self.assertEqual(expected, movelist)

    def test_scan_no_capture(self):
        b = Board("""
                    1 W
                    .....
                    .....
                    ..Qp.
                    .....
                    .....
                    .....
                    """)
        startpos = Position(3,4)
        
        # not capturing right
        movelist = b.scan(startpos, 1, 0, no_capture=True)
        expected = []
        self.assertEqual(expected, movelist)

        # to the top
        movelist = b.scan(startpos, 0, 1, no_capture=True)
        expected = []
        expected.append(Move.from_string("c4-c5"))
        expected.append(Move.from_string("c4-c6"))
        self.assertEqual(expected, movelist)

    def test_scan_no_capture_one_step(self):
        b = Board("""
                    1 W
                    .....
                    .....
                    ..Pp.
                    .....
                    .....
                    .....
                    """)
        startpos = Position(3,4)
        
        # to the top
        movelist = b.scan(startpos, 0, 1, no_capture=True, one_step=True)
        expected = []
        expected.append(Move.from_string("c4-c5"))
        self.assertEqual(expected, movelist)

        # not capturing right
        movelist = b.scan(startpos, 1, 0, no_capture=True, one_step=True)
        expected = []
        self.assertEqual(expected, movelist)

if __name__ == "__main__": 
    unittest.main()