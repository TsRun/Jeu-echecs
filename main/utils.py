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

def convert_move(move : str, board : list[list[Piece]]) -> str:
    if move[:2] == "sp":
        move = move[2:]
        if move[0]== "0":
            return move
        elif move[0] == "e":
            return f'{convert_coords(tuple(map(int, move[1:3])))[0]}x{convert_coords(tuple(map(int, move[3:])))}'
        elif move[0] == "p":
            return f'{convert_move(move[2:], board)} -> {move[1]}'
    else:
        piece = board[int(move[0])][int(move[1])]
        captured_piece = board[int(move[2])][int(move[3])]
        if piece.type == "pawn":
            piece_base = ""
        elif piece.type == "knight":
            piece_base = "N"
        else:
            piece_base = piece.type[0].upper()
        if captured_piece.color != "Neutral":
            return f'{piece_base}{convert_coords(tuple(map(int, move[0:2])))[0]}x{convert_coords(tuple(map(int, move[2:])))}'
        else:
            return f'{piece_base}{convert_coords(tuple(map(int, move[2:4])))}'
