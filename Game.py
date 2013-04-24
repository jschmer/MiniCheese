# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

from Player import HumanPlayer, SkirmishPlayer, RandomPlayer
from GreedyPlayer import GreedyPlayer
from NegamaxPlayer import NegamaxPlayer
from NegamaxPruningPlayer import NegamaxPruningPlayer
from Board import Board
from FancyDisplay import FancyDisplay
from Move import Move
import sys
import argparse

parser = argparse.ArgumentParser(description='Play a game of chess!')
parser.add_argument('playertypes', nargs=2, choices=['h', 'r', 'g', 'n', 'np', 'imcs'], help='playertype of white and black')
args = parser.parse_args()

# create players
players = {}
for i, color in enumerate(('white', 'black')):
    if args.playertypes[i] == 'h':
        players[color] = HumanPlayer()
    elif args.playertypes[i] == 'r':
        players[color] = RandomPlayer()
    elif args.playertypes[i] == 'g':
        players[color] = GreedyPlayer()
    elif args.playertypes[i] == 'n':
        players[color] = NegamaxPlayer()
    elif args.playertypes[i] == 'imcs':
        players[color] = SkirmishPlayer()
    elif args.playertypes[i] == 'np':
        players[color] = NegamaxPruningPlayer()



game = Board()
fancy = FancyDisplay()
move = Move.from_string("a1-a1") # dummy start move for fancy printing

while True:
    print(game)
    fancy.print(game)
    fancy.print_move(move)

    # check if any legal moves exist
    legal_moves = game.legal_moves()
    if not legal_moves:
        result = ("Black" if game.turn == "W" else "White") + " wins!"
        break
           
    # generate move       
    if game.turn == 'W':
        move = players['white'].generate_move(game)
    else:
        move = players['black'].generate_move(game)
   
    # check if move is legal
    if not move in legal_moves:
        print("Illegal move! Try again!")
        continue

    # send the move to opponent
    if game.turn == 'W':
        players['black'].process_opponent_move(move)
    else:
        players['white'].process_opponent_move(move)

    result = game.move(move)
    print("\n\nM: " + str(move))

    # skirmish wants the result
    for player in players.values():
        player.process_result(result)


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
fancy.print_move(move)
