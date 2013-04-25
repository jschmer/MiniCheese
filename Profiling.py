# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

from NegamaxPlayer import NegamaxPlayer
from NegamaxPruningPlayer import NegamaxPruningPlayer
from IterativeDeepeningPlayer import IterativeDeepeningPlayer
from Board import Board
import cProfile as cp

board = Board("""
                1 W
                kp...
                .p.N.
                r.n..
                q..R.
                .Q...
                ...K.
                """)

def runmegamax():
    player = NegamaxPlayer()
    best_move = player.negamax(board, 6)

def runPruning():
    player = NegamaxPruningPlayer()
    best_move = player.negamax(board, 6, -500000, 500000)

def runID():
    player = IterativeDeepeningPlayer()
    player.match_duration = 900
    best_move = player.generate_move(board)
    

if __name__ == '__main__':
    #cp.run("runmegamax()", sort="time")
    #cp.run("runPruning()", sort="time")
    cp.run("runID()", sort="time")