# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

from Board import Board
from Move import Move
from random import choice

game = Board()

while True:
    print("\n")
    print(game)

    legal_moves = game.legal_moves()
       
    if not legal_moves:
        winner = "Black" if game.turn == "W" else "White"
        print(winner + " wins!")
        break
     
    move = choice(legal_moves)
    status = game.move(move)

    if status == 'W':
        # white wins
        print("White wins with " + str(move) + "! Congrats!")
        break
    elif status == 'B':
        # black wins
        print("Black wins with " + str(move) + "! Congrats!")
        break
    elif status == '=':
        # draw
        print("A boring draw...")
        break
    else:
        # nothing happend, doh!
        pass

print(game)