from Board import Board
from Piece import Piece, Rook, Knight, Bishop, Queen
from utils import search, is_square_attack, is_check, convert_move
import tkinter as tk

class Move():

###############################################################################
#                                                                             #
#                            INITIALISATION                                   #
#                                                                             #
###############################################################################
    def __init__(self, canvas : tk.Canvas, last_position : 'Move' = None, last_move : str = "", root : tk.Tk = None):
        self.next = None
        self.nexts = []
        self._piece_selected = None
        self.is_the_actual = True
        if root is not None:
            self.root = root
            self.canvas = canvas
            self.base_init()
        else:
            self.prev = last_position
            self.last_move = last_move
            self.root = last_position.root
            self.canvas = last_position.canvas
            self.turn = "black" if last_position.turn == "white" else "white"
            self.board = Board(root=self.root, canvas=self.canvas, board=last_position.board.copy())
            self.after_move(self.board, last_move)
            #print(self.board)
            last_position.add_next(self)
        self.opposite_turn = "black" if self.turn == "white" else "white"
        self.king_position = search(self.board, "king", self.turn)

    def base_init(self):
        self.prev = None
        self.board = []
        self.turn = "white"
        self.last_move = ""
        self.board = Board(root=self.root, canvas=self.canvas)

    @property
    def piece_selected(self):
        return self._piece_selected

    @piece_selected.setter
    def piece_selected(self, piece):
        self._piece_selected = piece
        self.observe_piece(piece)

    def observe_piece(self, value):
        if value is None:
            self.canvas.delete("color_change")
        else:
            self.board.change_color_rectangle(value.position, "#F2C960", 1)

###############################################################################
#                                                                             #
#                               MAKE_MOVE                                     #
#                                                                             #
###############################################################################

    def check_checkmate(self) -> str:
        for i in range(8):
            for piece in self.board[i]:
                if piece.color == self.turn:
                    for j in range(8):
                        for k in range(8):
                            if self.is_legal((j, k), piece) != "":
                                #print(f"The first legal move is {piece.type} to {convert_coords(move)}")
                                return ""
        if is_check(self.board, self.turn):
            return "CheckMate"
        else:
            return "StaleMate"

    def do_move(self, move : str) -> 'Move':
        print(f'The move was {convert_move(move, self.board.board)}')
        self.piece_selected = None
        self.is_the_actual = False
        self.hide_board()
        return Move(canvas=self.canvas, last_position=self, last_move=move, root=None)

    def is_legal(self, position : tuple, piece : Piece) -> str:
        #print(self.board.board)
        if position not in piece.possible_moves(self.board.board):
            new_move = self.is_special_move(position, piece)
        elif piece.type == "pawn" and position[0] in [0, 7]:
            new_move = f'sppQ{piece.position[0]}{piece.position[1]}{position[0]}{position[1]}'
        else:
            new_move =f'{piece.position[0]}{piece.position[1]}{position[0]}{position[1]}'
        if new_move != "":
            temp_board = self.board.copy()
            self.after_move(temp_board, new_move)
            if is_check(temp_board, self.turn):
                self.piece_selected = None
                return ""
            else:
                return new_move
        return ""

    def is_special_move(self, position : tuple, piece : Piece) -> str:
        if piece.type == "king" and piece.has_moved is False:
            if (position[0] != 7 and self.turn == "white") or (position[0] != 0 and self.turn == "black"):
                return ""
            if position[1] >= 6:
                for i in range(piece.position[1], piece.position[1] + 3):
                    if is_square_attack((piece.position[0], i), self.board.board, self.opposite_turn):
                        return ""
                for i in range(piece.position[1] + 1, 8):
                    expected_rook = self.board[piece.position[0]][i]
                    if expected_rook.type == "rook" and expected_rook.color == piece.color and expected_rook.has_moved is False:
                        break
                    if self.board[piece.position[0]][i].color != "Neutral":
                        return ""
                return "sp0-0"
            elif position[1] <= 2:
                for i in range(piece.position[1] - 2, piece.position[1] + 1, -1):
                    if is_square_attack((piece.position[0], i), self.board.board, self.opposite_turn):
                        return ""
                for i in range(piece.position[1] - 1, -1, -1):
                    expected_rook = self.board[piece.position[0]][i]
                    if expected_rook.type == "rook" and expected_rook.color == piece.color and expected_rook.has_moved is False:
                        break
                    if self.board[piece.position[0]][i].color != "Neutral":
                        return ""
                return "sp0-0-0"
            else:
                return ""
        elif piece.type == "pawn":
            if abs(position[1] - piece.position[1]) == 1 and position[0] == piece.position[0] + piece.direction and self.board[position[0]][position[1]].color == "Neutral" and self.last_move == f'{position[0] + piece.direction}{position[1]}{piece.position[0]}{position[1]}':
                return f'spe{piece.position[0]}{piece.position[1]}{position[0]}{position[1]}'
        return ""

    def after_move(self, board : list[list[Piece]], current_move : str):
        if current_move[0:2] == "sp":
            self.special_move(board, current_move[2:])
        else:
            piece = board[int(current_move[0])][int(current_move[1])]
            piece.position = (int(current_move[2]), int(current_move[3]))
            piece.has_moved = True
            board[int(current_move[2])][int(current_move[3])] = piece
            board[int(current_move[0])][int(current_move[1])] = Piece("", (int(current_move[0]), int(current_move[1])), "")

    def special_move(self, board : Board, current_move : str):
        if current_move == "0-0":
            if self.turn == "black":
                self.after_move(board, "7476")
                self.after_move(board, "7775")
            else:
                self.after_move(board, "0406")
                self.after_move(board, "0705")
        elif current_move == "0-0-0":
            if self.turn == "black":
                self.after_move(board, "7472")
                self.after_move(board, "7073")
            else:
                self.after_move(board, "0402")
                self.after_move(board, "0003")
        elif current_move[0] == "p":
            promotions = {'Q' : Queen, 'R' : Rook, 'N' : Knight, 'B' : Bishop}
            color = board[int(current_move[2])][int(current_move[3])].color
            board[int(current_move[4])][int(current_move[5])] = promotions[current_move[1]](color, (int(current_move[4]), int(current_move[5])))
            board[int(current_move[2])][int(current_move[3])] = Piece("", (int(current_move[2]), int(current_move[3])), "")
        elif current_move[0] == "e":
            piece = board[int(current_move[1])][int(current_move[2])]
            board[int(current_move[3]) - piece.direction][int(current_move[4])] = Piece("", (int(current_move[3]) - piece.direction, int(current_move[4])), "")
            self.after_move(board, current_move[1:])
        else:
            print("error")

###############################################################################
#                                                                             #
#                                  UTILS                                      #
#                                                                             #
###############################################################################


    def add_next(self, next_move : 'Move'):
        self.nexts.append(next_move)
        if self.next is None:
            self.next = next_move

    #Utils
    def show_board(self):
        self.board.show_board()

    def hide_board(self):
        self.board.canvas.delete("piece")

###############################################################################
#                                                                             #
#                                 BOUTON                                      #
#                                                                             #
###############################################################################

    def on_click(self, event) -> 'Move':
        x, y = int(event.x // (self.board.board_size / 8)), int(event.y // (self.board.board_size / 8))
        #print(f'You clicked in {convert_coords((y,x))}')
        if self.piece_selected is None:
            if self.board[y][x].color == self.turn:
                self.piece_selected = self.board[y][x]
            #print(f'You selected {self.piece_selected.type} at {convert_coords(self.piece_selected.position)}')
        elif (y, x) != self.piece_selected.position:
            #print(f'You want to move {self.piece_selected.type} to {convert_coords((y,x))}')
            new_move = self.is_legal((y, x), self.piece_selected)
            if new_move != "":
                return self.do_move(new_move)
            print('Not a legal move')
            self.piece_selected = None
        return self

    def on_release(self, event) -> 'Move':
        if self.piece_selected is None:
            return self
        x, y = int(event.x // (self.board.board_size / 8)), int(event.y // (self.board.board_size / 8))
        #print(f'You clicked in {convert_coords((y,x))}')
        self.reset_piece()
        if (y, x) != self.piece_selected.position:
            #print(f'You want to move {self.piece_selected.type} to {convert_coords((y,x))}')
            new_move = self.is_legal((y, x), self.piece_selected)
            if new_move != "":
                return self.do_move(new_move)
            print('Not a legal move')
        return self

    def on_drag(self, event):
        x, y = event.x - 40, event.y - 40
        if self.piece_selected is not None:
            self.board.canvas.coords(self.piece_selected.ImageID, x, y)

    def reset_piece(self):
        if self.piece_selected is None:
            return
        old_x, old_y = map(lambda x:x * (self.board.board_size / 8), self.piece_selected.position)
        self.board.canvas.coords(self.piece_selected.ImageID, old_y, old_x)

    def on_right_click(self, event):
        self.reset_piece()
        self.piece_selected = None
