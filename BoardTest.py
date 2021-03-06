# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

import unittest 
from Board import Board
from Move import Move

class BoardTest(unittest.TestCase):

    def test_fields(self):
        b = Board("""
            11 W
            p.bn.
            .....
            .....
            .....
            .....
            ...QK
            """)
        fields = [p for p in b.fields()]
        fields = "".join(fields)
        expected = "...QK....................p.bn."
        self.assertEqual(expected, fields)

    def test_construct_default(self): 
        b = Board()

        self.assertEqual(b.board, [list("RNBQK"),
                                   list("PPPPP"),
                                   list("....."),
                                   list("....."),
                                   list("ppppp"),
                                   list("kqbnr")])
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
        self.assertEqual(b.board, [list("RNBQK"),
                                   list("..PPP"),
                                   list("PP..."),
                                   list("....."),
                                   list("pp..."),
                                   list("..bn.")])
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

    def test_construct_from_other(self):
        b = Board("""
            11 W
            ..bn.
            pp...
            .....
            PP...
            ..PPP
            RNBQK
            """)
        b.move(Move.from_string("a1-a2"))
        b2 = Board.from_other(b)
        self.assertEqual(b, b2)
        self.assertEqual(b.history, b2.history)
        


    def test_string_representation(self):
        b = Board()
        self.assertEqual(str(b), "1 W\nkqbnr\nppppp\n.....\n.....\nPPPPP\nRNBQK")

    def test_is_within_bounds(self):
        b = Board()
        pos = (0, 0)
        self.assertFalse(b.is_within_bounds(pos))

        pos = (1, 1)
        self.assertTrue(b.is_within_bounds(pos))

        pos = (5, 6)
        self.assertTrue(b.is_within_bounds(pos))

        pos = (6, 6)
        self.assertFalse(b.is_within_bounds(pos))

        pos = (5, 7)
        self.assertFalse(b.is_within_bounds(pos))

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

        move = Move((1,2), (1,3))
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

        move = Move((1,2), (1,3))
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
            ...kK
            """)

        b1.move(Move.from_string("a5-a6"))
        b2 = Board("""
            1 B
            Q....
            .....
            .....
            .....
            .....
            ...kK
            """)
        self.assertEqual(b1, b2)

        b3 = Board("""
            1 B
            k....
            .....
            .....
            .....
            ..p..
            ...K.
            """)
        b3.move(Move.from_string("c2-d1"))
        b4 = Board("""
            2 W
            k....
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

        b4 = Board("""
            1 W
            kqbnr
            ppppp
            .....
            .....
            PPPPP
            RNBQK
            """)
        b4.cur_score = 123
        self.assertFalse(b == b4)

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
        startpos = (3,4)
        
        # to the right
        movelist = []
        b.scan(movelist, startpos, 1, 0)
        expected = []
        expected.append(Move.from_string("c4-d4"))
        expected.append(Move.from_string("c4-e4"))
        self.assertEqual(expected, movelist)

        # to the left
        movelist = []
        b.scan(movelist, startpos, -1, 0)
        expected = []
        expected.append(Move.from_string("c4-b4"))
        expected.append(Move.from_string("c4-a4"))
        self.assertEqual(expected, movelist)

        # to the top
        movelist = []
        b.scan(movelist, startpos, 0, 1)
        expected = []
        expected.append(Move.from_string("c4-c5"))
        expected.append(Move.from_string("c4-c6"))
        self.assertEqual(expected, movelist)

        # to the bottom
        movelist = []
        b.scan(movelist, startpos, 0, -1)
        expected = []
        expected.append(Move.from_string("c4-c3"))
        expected.append(Move.from_string("c4-c2"))
        expected.append(Move.from_string("c4-c1"))
        self.assertEqual(expected, movelist)

        # diagonal left top
        movelist = []
        b.scan(movelist, startpos, -1, 1)
        expected = []
        expected.append(Move.from_string("c4-b5"))
        expected.append(Move.from_string("c4-a6"))
        self.assertEqual(expected, movelist)

        # diagonal right top
        movelist = []
        b.scan(movelist, startpos, 1, 1)
        expected = []
        expected.append(Move.from_string("c4-d5"))
        expected.append(Move.from_string("c4-e6"))
        self.assertEqual(expected, movelist)

        # diagonal right bottom
        movelist = []
        b.scan(movelist, startpos, 1, -1)
        expected = []
        expected.append(Move.from_string("c4-d3"))
        expected.append(Move.from_string("c4-e2"))
        self.assertEqual(expected, movelist)

        # diagonal left bottom
        movelist = []
        b.scan(movelist, startpos, -1, -1)
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
        startpos = (3,4)
        
        movelist = []
        b.scan(movelist, startpos, 1, 1)
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
        startpos = (1,1)
        
        movelist = []
        b.scan(movelist, startpos, 1, 1)
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
        startpos = (2,3)
        
        # capturing right
        movelist = []
        b.scan(movelist, startpos, 1, 0, one_step=True)
        expected = []
        expected.append(Move.from_string("b3-c3"))
        self.assertEqual(expected, movelist)

        # to the top
        movelist = []
        b.scan(movelist, startpos, 0, 1, one_step=True)
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
        startpos = (3,4)
        
        # to the top
        movelist = []
        b.scan(movelist, startpos, 0, 1, only_capture=True)
        expected = []
        self.assertEqual(expected, movelist)

        # capturing enemy
        movelist = []
        b.scan(movelist, startpos, 1, 1, only_capture=True)
        expected = []
        expected.append(Move.from_string("c4-d5"))
        self.assertEqual(expected, movelist)

        # not capturing own
        movelist = []
        b.scan(movelist, startpos, 0, -1, only_capture=True)
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
        startpos = (3,4)
        
        # not capturing right
        movelist = []
        b.scan(movelist, startpos, 1, 0, no_capture=True)
        expected = []
        self.assertEqual(expected, movelist)

        # to the top
        movelist = []
        b.scan(movelist, startpos, 0, 1, no_capture=True)
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
        startpos = (3,4)
        
        # to the top
        movelist = []
        b.scan(movelist, startpos, 0, 1, no_capture=True, one_step=True)
        expected = []
        expected.append(Move.from_string("c4-c5"))
        self.assertEqual(expected, movelist)

        # not capturing right
        movelist = []
        b.scan(movelist, startpos, 1, 0, no_capture=True, one_step=True)
        expected = []
        self.assertEqual(expected, movelist)

    def test_legal_moves_rook(self):
        b = Board("""
                    1 W
                    .....
                    .....
                    ..Rr.
                    .....
                    .....
                    .....
                    """)
        
        # get legal moves for white rook 'R'
        legal_moves = b.legal_moves()

        expected = []
        expected.append(Move.from_string("c4-d4"))
        expected.append(Move.from_string("c4-c3"))
        expected.append(Move.from_string("c4-c2"))
        expected.append(Move.from_string("c4-c1"))
        expected.append(Move.from_string("c4-b4"))
        expected.append(Move.from_string("c4-a4"))
        expected.append(Move.from_string("c4-c5"))
        expected.append(Move.from_string("c4-c6"))

        self.assertEqual(len(expected), len(legal_moves))
        for move in expected:
            self.assertIn(move, legal_moves)

    def test_legal_moves_pawn(self):
        b = Board("""
                    1 W
                    .....
                    .....
                    ..P..
                    .....
                    .....
                    .....
                    """)
        
        # get legal moves for white pawn 'P'
        legal_moves = b.legal_moves()

        expected = []
        expected.append(Move.from_string("c4-c5"))

        self.assertEqual(len(expected), len(legal_moves))
        for move in expected:
            self.assertIn(move, legal_moves)

        b = Board("""
                    1 W
                    .....
                    ...r.
                    ..P..
                    .....
                    .....
                    .....
                    """)
        startpos = (3,4) #c4
        
        # get legal moves for white pawn 'P'
        legal_moves = b.legal_moves()

        expected = []
        expected.append(Move.from_string("c4-c5"))
        expected.append(Move.from_string("c4-d5"))

        self.assertEqual(len(expected), len(legal_moves))
        for move in expected:
            self.assertIn(move, legal_moves)

        b = Board("""
                    1 B
                    .....
                    ..p..
                    ..R..
                    .....
                    .....
                    .....
                    """)
        startpos = (3,5) #c5
        
        # get legal moves for black pawn 'p'
        legal_moves = b.legal_moves()

        expected = []

        self.assertEqual(len(expected), len(legal_moves))
        for move in expected:
            self.assertIn(move, legal_moves)

        b = Board("""
                    1 B
                    .....
                    ..p..
                    .P...
                    .....
                    .....
                    .....
                    """)
        startpos = (3,5) #c5
        
        # get legal moves for black pawn 'p'
        legal_moves = b.legal_moves()

        expected = []
        expected.append(Move.from_string("c5-c4"))
        expected.append(Move.from_string("c5-b4"))

        self.assertEqual(len(expected), len(legal_moves))
        for move in expected:
            self.assertIn(move, legal_moves)

    def test_legal_moves_king(self):
        b = Board("""
                    1 W
                    .....
                    .....
                    .....
                    .....
                    p....
                    K....
                    """)
        
        # get legal moves for white king 'K'
        legal_moves = b.legal_moves()

        expected = []
        expected.append(Move.from_string("a1-a2"))
        expected.append(Move.from_string("a1-b1"))
        expected.append(Move.from_string("a1-b2"))

        self.assertEqual(len(expected), len(legal_moves))
        for move in expected:
            self.assertIn(move, legal_moves)

    def test_legal_moves_bishop(self):
        b = Board("""
                    1 W
                    .....
                    .....
                    ...p.
                    .p...
                    .B...
                    .....
                    """)
        
        # get legal moves for white bishop 'B'
        legal_moves = b.legal_moves()

        expected = []
        expected.append(Move.from_string("b2-a1"))
        expected.append(Move.from_string("b2-c3"))
        expected.append(Move.from_string("b2-d4"))
        expected.append(Move.from_string("b2-a3"))
        expected.append(Move.from_string("b2-c1"))
        
        expected.append(Move.from_string("b2-b1"))
        expected.append(Move.from_string("b2-a2"))
        expected.append(Move.from_string("b2-c2"))

        self.assertEqual(len(expected), len(legal_moves))
        for move in expected:
            self.assertIn(move, legal_moves)

    def test_legal_moves_knight(self):
        b = Board("""
                    1 W
                    .....
                    .....
                    .....
                    .p...
                    .....
                    N....
                    """)

        # get legal moves for white knight 'N'
        legal_moves = b.legal_moves()

        expected = []
        expected.append(Move.from_string("a1-b3"))
        expected.append(Move.from_string("a1-c2"))

        self.assertEqual(len(expected), len(legal_moves))
        for move in expected:
            self.assertIn(move, legal_moves)

    def test_legal_moves_combined(self):
        b = Board("""
                    1 W
                    ..k..
                    q..p.
                    .....
                    .P...
                    ....r
                    N...K
                    """)

        # get legal moves for all white pieces
        legal_moves = b.legal_moves()

        expected = []
        # knight
        expected.append(Move.from_string("a1-c2"))
        # king
        expected.append(Move.from_string("e1-e2"))
        expected.append(Move.from_string("e1-d2"))
        expected.append(Move.from_string("e1-d1"))
        # pawn
        expected.append(Move.from_string("b3-b4"))

        self.assertEqual(len(expected), len(legal_moves))
        for move in expected:
            self.assertIn(move, legal_moves)
    
    def test_get_score(self):
        b = Board("""
            1 W
            ..k..
            q..p.
            .....
            .P...
            ....r
            N...K
            """)
        self.assertEqual(b.score(), -1160)

        b = Board("""
            1 B
            ..k..
            q..p.
            .....
            .P...
            ....r
            N....
            """)
        self.assertEqual(b.score(), 100000)

    def test_move_and_score(self):
        b = Board("""
            1 W
            ..k..
            q..p.
            .....
            .P...
            ....r
            N...K
            """)
        self.assertEqual(b.score(), -1160) # score for white!

        # moving pawn, no change in score, Black has advantage
        b.move(Move.from_string("b3-b4"))
        self.assertEqual(b.score(), 1150) # score for black!

        # capturing white king, changed score! White is losing
        b.move(Move.from_string("e2-e1"))
        self.assertEqual(b.score(), -100000) # score for white!

        b = Board("""
            1 W
            ..k..
            q..P.
            .....
            .p...
            ....r
            N...K
            """)
        self.assertEqual(b.score(), -1160) # score for white!

        # white moving knight, captures pawn, white gains points
        b.move(Move.from_string("a1-b3"))
        self.assertEqual(b.score(), 995) # score for black!

        # black moving queen, doing nothing!
        b.move(Move.from_string("a5-a4"))
        self.assertEqual(b.score(), -995) # score for white!

        # white promoting its pawn! gaining points!
        b.move(Move.from_string("d5-d6"))
        self.assertEqual(b.score(), 250) # score for black!

        # black capturing knight, gaining points!
        b.move(Move.from_string("a4-b3"))
        self.assertEqual(b.score(), -510) # score for white!

        # white capturing king! gaining points!
        b.move(Move.from_string("d6-c6"))
        self.assertEqual(b.score(), -100000) # score for black!

        return
        # test a drawing game
        b = Board("""
            40 W
            ..k..
            .p...
            .....
            .....
            Q....
            ....K
            """)
        self.assertEqual(b.score(), 800) # score for white!
        
        b.move(Move.from_string("a2-a3"))
        self.assertEqual(b.score(), -800) # score for black!
        
        b.move(Move.from_string("b5-b4"))
        self.assertEqual(b.score(), 0) # score for white!

    def test_try_move_and_score(self):
        b = Board("""
            1 W
            ..k..
            q..p.
            .....
            .P...
            ....r
            N...K
            """)
        self.assertEqual(b.score_after(Move.from_string("b3-b4")), 1150) # score for black!

        # moving pawn, no change in score, Black has advantage
        b.move(Move.from_string("b3-b4"))
        self.assertEqual(b.score_after(Move.from_string("e2-e1")), -100000) # score for white!

    def test_at(self):
        b = Board()
        self.assertEqual('R', b.at((1, 1)))

    def test_set(self):
        b = Board()
        b.set((1, 1), '.')
        self.assertEqual('.', b.at((1, 1)))

    def test_undo_last_move(self):
        b = Board("""
            1 W
            ...k.
            ..P..
            .....
            .....
            .....
            .....
            """)
        b2 = Board("""
            1 W
            ...k.
            ..P..
            .....
            .....
            .....
            .....
            """)

        b.move(Move.from_string("c5-c6"))
        b.undo_last_move()
        self.assertEqual(b, b2)

        b.move(Move.from_string("c5-d6"))
        b.undo_last_move()
        self.assertEqual(b, b2)

    def test_bonus_score(self):
        b = Board()

        # white pawn default position
        bonus = b._bonus_score((1,2), 'P')
        self.assertEqual(10, bonus)

        # black pawn default position
        bonus = b._bonus_score((1,5), 'p')
        self.assertEqual(-10, bonus)

if __name__ == "__main__": 
    unittest.main()