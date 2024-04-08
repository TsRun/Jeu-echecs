from Piece import *

def convert_coords(coords : tuple):
    y = 8 - coords[0]
    x = chr(97 + coords[1])
    return x + str(y)

def search(board, piece_type : str, color : str):
    for i in range(8):
        for piece in board[i]:
            if piece.color == color and piece.type == piece_type:
                return piece.position

def is_square_attack(position : tuple[int, int], board : list[list[Piece]], color : str) -> bool:
    for i in range(8):
        for piece in board[i]:
            if piece.color == color and position in piece.possible_moves(board):
                return True
    return False

def opposite_color(color : str) -> str:
    return "white" if color == "black" else "black"

def is_check(board : list[list[Piece]], color : str) -> bool:
    king_position = search(board, "king", color)
    return is_square_attack(king_position, board, opposite_color(color))

