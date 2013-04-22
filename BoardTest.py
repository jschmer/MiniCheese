import unittest 
import Board

class BoardTest(unittest.TestCase):

    def construct(self): 
        b = Board.Board()

        self.assertEqual(b.board, [
                                       "kqbnr",
                                       "ppppp",
                                       ".....",
                                       ".....",
                                       "PPPPP",
                                       "RNBQK"
                                       ]) 
        pass

print("BoardTest")

if __name__ == "__main__": 
    unittest.main()