from tkinter import *
from Position import Position

master = Tk()

path_prefix = "chess_pieces\\"

piece_keys = "kqrbnpKQRBNPsS"

piece_img = {}
# images for chess pieces
piece_img['k'] = PhotoImage(file=path_prefix + "king_black.gif")
piece_img['K'] = PhotoImage(file=path_prefix + "king_white.gif")
piece_img['q'] = PhotoImage(file=path_prefix + "queen_black.gif")
piece_img['Q'] = PhotoImage(file=path_prefix + "Queen_white.gif")
piece_img['r'] = PhotoImage(file=path_prefix + "rook_black.gif")
piece_img['R'] = PhotoImage(file=path_prefix + "rook_white.gif")
piece_img['b'] = PhotoImage(file=path_prefix + "bishop_black.gif")
piece_img['B'] = PhotoImage(file=path_prefix + "bishop_white.gif")
piece_img['n'] = PhotoImage(file=path_prefix + "knight_black.gif")
piece_img['N'] = PhotoImage(file=path_prefix + "knight_white.gif")
piece_img['p'] = PhotoImage(file=path_prefix + "pawn_black.gif")
piece_img['P'] = PhotoImage(file=path_prefix + "pawn_white.gif")

# images for board squares
piece_img['s'] = PhotoImage(file=path_prefix + "square_black.gif")
piece_img['S'] = PhotoImage(file=path_prefix + "square_white_border.gif")

class FancyDisplay(object):
    canvas_width  = 350
    canvas_height = 420
    piece_side = 70
  
    def __init__(self):
        self.canvas = Canvas(master, 
                   width  = FancyDisplay.canvas_width, 
                   height = FancyDisplay.canvas_height)
        self.canvas.pack()

    def draw_piece_at(self, x, y, piece):
        side_len = FancyDisplay.piece_side

        if piece in piece_keys:
            self.canvas.create_image(x*side_len, (5-y)*side_len, anchor=NW, image=piece_img[piece])

    def print(self, game):
        self.print_board()
        self.print_pieces(game)
        self.update()

    def print_board(self):
        side_len = FancyDisplay.piece_side

        black = True
        for y in range(0, 6):
            for x in range(0, 5):
                if black:
                    self.draw_piece_at(x, y, 'S')
                else:
                    self.draw_piece_at(x, y, 'S')
                black = not black

    def print_pieces(self, board):
        for row in range(1, 7):
            for col in range(1, 6):
                position = Position(col, row)
                field = board.piece_at(position)
                self.draw_piece_at(col-1, row-1, field)

    def update(self):
        master.update()
