# python skirmish/skirmish.py imcs://MiniCheese:cheese@svcs.cs.pdx.edu:3589/accept?id=6260 "run python3 Game.py imcs np"
# python skirmish/skirmish.py "run python3 Game.py np imcs" imcs://MiniCheese:cheese@svcs.cs.pdx.edu:3589/accept?id=6255

# PlayOnline.py w 6200 np
import argparse
import sys
import subprocess

parser = argparse.ArgumentParser(description='Play a game of chess online!')
parser.add_argument('-o', '--offer', action="store_true")
parser.add_argument('-a', '--accept', metavar='id')
parser.add_argument('color', choices=['w', 'b'])
parser.add_argument('our_player', help='command line arguments to our player')
args = parser.parse_args()

BASE_URL = "imcs://MiniCheese:cheese@svcs.cs.pdx.edu:3589" 
ACCEPT = "/accept?id={id}"
OFFER = "/offer"


## Skirmish command line arguments
# Players white and black can be one of the following options:
    
#   "-"                       (communicate with standard in/out)
    
#   "run COMMAND"             (use standard in/out of the specified shell command)
    
#   "imcs://user:pass@host:port/PATH", where path is one of:
#       /offer                (offer a game of the player's color)
#       /accept?arg=val[&..]  (accept game with the following allowed parameters)
#         id=N                  (game has id number N)
#         name=STR              (player has name STR)
#         rating=N              (player has rating N)
# """

commandline = ["python2", "skirmish/skirmish.py", "-v"]

# commandline for our player
our_player_cmd = ["run", "python3", "Game.py"]
if args.color == 'w':
    our_player_cmd += [args.our_player, 'skirmish']
else:
    our_player_cmd += ['skirmish', args.our_player]
our_player_cmd = " ".join(our_player_cmd)

# commandline for the server player
imcs_player_cmd = BASE_URL
if args.offer:
    imcs_player_cmd += OFFER
elif args.accept:
    imcs_player_cmd += ACCEPT.format(id=args.accept)
else:
    print("you have to either specifie accept or offer")
    sys.exit(0)

# final commandline for skirmish
if args.color == 'w':
    commandline.append(our_player_cmd)
    commandline.append(imcs_player_cmd)
else:
    commandline.append(imcs_player_cmd)
    commandline.append(our_player_cmd)

subprocess.call(commandline)