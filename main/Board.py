from Piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King
import tkinter as tk
from PIL import Image, ImageTk
from utils import convert_coords

colors = ["#F0D9B5", "#B58863"]

class Board(tk.Canvas):

###############################################################################
#                                                                             #
#                            INITIALISATION                                   #
#                                                                             #
###############################################################################
    def __init__(self, root : tk.Tk, board : list[list[Piece]] = None):
        if board is None:
            board = self.init_pieces()
        self.root = root
        self.board = board
        self.board_size = min(root.winfo_width(), root.winfo_height()) - 40
        self.canvas = tk.Canvas(self.root, width=self.board_size, height=self.board_size)

    def init_pieces(self) -> list[list[Piece]]:
        board = [
            [], [], [], [], [], [], [], []
        ]
        board[0] = [Rook("black", (0, 0)), Knight("black", (0, 1)), Bishop("black", (0, 2)), Queen("black", (0, 3)), King("black", (0, 4)), Bishop("black", (0, 5)), Knight("black", (0, 6)), Rook("black", (0, 7))]
        board[1] = [Pawn("black", (1, i)) for i in range(8)]
        for i in range(2, 6):
            board[i] = [Piece("", (i, j), "") for j in range(8)]
        board[6] = [Pawn("white", (6, i)) for i in range(8)]
        board[7] = [Rook("white", (7, 0)), Knight("white", (7, 1)), Bishop("white", (7, 2)), Queen("white", (7, 3)), King("white", (7, 4)), Bishop("white", (7, 5)), Knight("white", (7, 6)), Rook("white", (7, 7))]
        return board

    def init_canvas(self) -> None:
        self.init_board()

    def init_board(self) -> None:
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    self.canvas.create_rectangle(j*self.board_size / 8, i*self.board_size / 8, (j + 1) * self.board_size / 8, (i + 1) * self.board_size / 8, fill=colors[0], tags="square")
                else:
                    self.canvas.create_rectangle(j*self.board_size / 8, i*self.board_size / 8, (j + 1) * self.board_size / 8, (i + 1) * self.board_size / 8, fill=colors[1], tags="square")
        self.resize_pieces()


###############################################################################
#                                                                             #
#                                  COLOR                                      #
#                                                                             #
###############################################################################

    def change_color_rectangle(self, position : tuple, color : str, transparent : int):
        self.canvas.create_rectangle(position[1]*self.board_size / 8, position[0]*self.board_size / 8, (position[1] + 1) * self.board_size / 8, (position[0] + 1) * self.board_size / 8, fill=color, tags="color_change")

    def reset_color(self):
        self.canvas.delete("color_change")

    def blink_square(self, position : tuple, color : str, alpha = 0):
        square = self.square_board[position[0]][position[1]]
        old_color = "white" if (position[0] + position[1]) % 2 == 0 else "green"
        if not self.blink_eneble:
            self.canvas.itemconfig(square, fill = old_color)
        else:
            colors = [old_color, color]
            self.canvas.itemconfig(square, fill = colors[self.color_index])
            if (alpha != 0):
                self.color_index = (self.color_index + 1) % 2
            else:
                self.color_index = 1
            self.root.after(int(500 * ((1 - alpha) if self.color_index == 0 else alpha)), self.blink_square, position, color, alpha)

###############################################################################
#                                                                             #
#                                  RESIZE                                     #
#                                                                             #
###############################################################################

    def resize(self) -> None:
        self.canvas.delete("all")
        self.init_board()

    def resize_pieces(self) -> None:
        for i in range(8):
            j = 0
            for piece in self.board[i]:
                j += 1
                if piece.color == "Neutral":
                    continue
                #print(f'{piece.type} {piece.color} {convert_coords(piece.position)} / {convert_coords((i, j - 1))}')
                piece.image = Image.open(piece.image_path)
                piece.image = piece.image.resize((int(self.board_size / 8), int(self.board_size / 8)))
                piece.tkimage = ImageTk.PhotoImage(piece.image)
                piece.ImageID = self.canvas.create_image(piece.position[1] * self.board_size / 8, piece.position[0] * self.board_size / 8, image=piece.tkimage, anchor="nw", tags="piece")


###############################################################################
#                                                                             #
#                                  UTILS                                      #
#                                                                             #
###############################################################################

    def show_board(self):
        if min(self.root.winfo_width(), self.root.winfo_height()) - 40 == self.board_size:
            self.canvas.pack()
        else:
            self.board_size = min(self.root.winfo_width(), self.root.winfo_height()) - 40
            self.resize()


    def __getitem__(self, position : int) -> Piece:
        return self.board[position]

    def __str__(self) -> str:
        string = ""
        for i in range(8):
            string += str(list(x.type for x in self.board[i])) + ("\n" if i != 8 else "")
        return string

    def copy(self) -> list[list[Piece]]:
        new_board = [
            [], [], [], [], [], [], [], []
        ]
        for i in range(8):
            for piece in self.board[i]:
                new_board[i].append(piece.copy())
        return new_board
