# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

from Board import Board
from Move import Move

game = Board()

while True:
    print("\n")
    print(game)
    a = input("Cmd: ").strip()

    if not a:
        continue
    if a == "exit":
        break

    try:
        human_move = Move.from_string(a)
        legal_moves = game.legal_moves()
        
        if not human_move in legal_moves:
            raise ValueError("Invalid move!")

        status = game.move(human_move)

        if status == 'W':
            # white wins
            print("White wins! Congrats!")
            break
        elif status == 'B':
            # black wins
            print("Black wins! Congrats!")
            break
        elif status == '=':
            # draw
            print("A boring draw...")
            break
        else:
            # nothing happend, doh!
            pass
    except ValueError:
        print("Invalid move! Try again!")