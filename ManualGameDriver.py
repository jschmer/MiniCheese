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
        game.move(Move.from_string(a))
    except ValueError:
        print("Invalid move! Try again!")