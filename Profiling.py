# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

from NegamaxPlayer import NegamaxPlayer
from NegamaxPruningPlayer import NegamaxPruningPlayer
from Board import Board
import cProfile as cp

def runmegamax():
    board = Board("""
                    1 W
                    kp...
                    .p...
                    .....
                    .....
                    .Q...
                    ...K.
                    """)
    board = Board()
    player = NegamaxPlayer()
    best_move = player.negamax(board, 6)

def runPruning():
    board = Board("""
                    1 W
                    kp...
                    .p...
                    .....
                    .....
                    .Q...
                    ...K.
                    """)
    board = Board()
    player = NegamaxPruningPlayer()
    best_move = player.negamax(board, 6, -500000, 500000)

    

if __name__ == '__main__':
    cp.run("runmegamax()", sort="time")
    cp.run("runPruning()", sort="time")