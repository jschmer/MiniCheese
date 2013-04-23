# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

from RandomPlayer import RandomPlayer
from HumanPlayer import HumanPlayer
from GreedyPlayer import GreedyPlayer
from NegamaxPlayer import NegamaxPlayer
from Board import Board
from FancyDisplay import FancyDisplay
import sys

# parse script arguments
player_param = sys.argv[1:]
if len(player_param) >= 1:
    param0 = player_param[0]
else:
    param0 = 'r'

if len(player_param) >= 2:
    param1 = player_param[1]
else:
    param1 = 'r'

# create players
if param0 == 'h':
    white = HumanPlayer()
elif param0 == 'r':
    white = RandomPlayer()
elif param0 == 'g':
    white = GreedyPlayer()
elif param0 == 'n':
    white = NegamaxPlayer()

if param1 == 'h':
    black = HumanPlayer()
elif param1 == 'r':
    black = RandomPlayer()
elif param1 == 'g':
    black = GreedyPlayer()
elif param1 == 'n':
    black = NegamaxPlayer()

game = Board()
fancy = FancyDisplay()

while True:
    print(game)
    fancy.print(game)

    # check if any legal moves exist
    legal_moves = game.legal_moves()
    if not legal_moves:
        result = ("Black" if game.turn == "W" else "White") + " wins!"
        break
           
    # generate move       
    if game.turn == 'W':
        move = white.generate_move(game)
    else:
        move = black.generate_move(game)
        pass
    
    # check if move is legal
    if not move in legal_moves:
        print("Illegal move! Try again!")
        continue

    result = game.move(move)
    print("\n\nM: " + str(move))

    # check result
    if result == 'W':
        # white wins
        result = "White wins with " + str(move) + "! Congrats!"
        break
    elif result == 'B':
        # black wins
        result = "Black wins with " + str(move) + "! Congrats!"
        break
    elif result == '=':
        # draw
        result = "A boring draw..."
        break
    else:
        # nothing exciting happend, doh!
        pass

print("#-#-#-#-#-#-#-#-#-#-#-#")
print(result)
print(game)
fancy.print(game)
input()