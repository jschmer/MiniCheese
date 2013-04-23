# -*- coding: utf-8 -*-
# Copyright © 2013 Jens Schmer, Michael Engelhard

# (dx, dy, only_capture, no_capture, one_step)
k = [(0, 1, False, False, True), 
     (0, -1, False, False, True), 
     (1, 0, False, False, True), 
     (1, 1, False, False, True), 
     (1, -1, False, False, True), 
     (-1, 0, False, False, True), 
     (-1, 1, False, False, True), 
     (-1, -1, False, False, True)]
K = k


q = [(0, 1, False, False, False), 
     (0, -1, False, False, False), 
     (1, 0, False, False, False), 
     (1, 1, False, False, False), 
     (1, -1, False, False, False), 
     (-1, 0, False, False, False), 
     (-1, 1, False, False, False), 
     (-1, -1, False, False, False)]
Q = q

b = [(1, 1, False, False, False), 
     (1, -1, False, False, False), 
     (-1, 1, False, False, False), 
     (-1, -1, False, False, False),
     (0, 1, False, True, True), 
     (0, -1, False, True, True), 
     (1, 0, False, True, True), 
     (-1, 0, False, True, True)]
B = b

# .n.n.
# n...n
# ..N..
# n...n
# .n.n.

# first row
n = [(-1, 2, False, False, False),
     (1, 2, False, False, False),
# second row
     (-2, 1, False, False, False),
     (2, 1, False, False, False),
# forth row
     (-2, -1, False, False, False),
     (2, -1, False, False, False),
# fifth
     (-1, -2, False, False, False),
     (1, -2, False, False, False)]
N = n

r = [(0, 1, False, False, False), 
     (0, -1, False, False, False), 
     (1, 0, False, False, False), 
     (-1, 0, False, False, False)]
R = r

# black pawn can only move down
p = [(0, -1, False, True, True), 
     (-1, -1, True, False, True), 
     (1, -1, True, False, True)]

# white pawn can only move up
P = [(0, 1, False, True, True), 
     (-1, 1, True, False, True), 
     (1, 1, True, False, True)]


scan_arguments = {
    'k': k,
    'q': q,
    'b': b,
    'n': n,
    'r': r,
    'p': p,
    'K': K,
    'Q': Q,
    'B': B,
    'N': N,
    'R': R,
    'P': P
}