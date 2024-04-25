from PIL import Image, ImageTk

class Piece:
    def __init__(self, color : str, position : tuple, image_path : str) -> None:
        self.has_moved = False
        self.direction = None
        self.position = position
        if color == "":
            self.image = None
            self.color = "Neutral"
            self.opposite_color = "Neutral"
            self.type = "Empty"
            self.image_path = None
            self.tkimage = None
            self.ImageID = None
            return
        self.opposite_color = "black" if color == "white" else "white"
        self.color = color
        self.type = image_path.split("/")[-1].split(".")[0].split('_')[1]
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.tkimage = ImageTk.PhotoImage(self.image)
        self.ImageID = None

    def possible_moves(self, board : list[list['Piece']]):
        pass

    def copy(self):
        return Piece("", self.position, "")

class Pawn(Piece):
    def __init__(self, color : str, position : tuple) -> None:
        Piece.__init__(self, color, position, "images/" + color + "_pawn.png")
        self.direction = -1 if color == "white" else 1

    def possible_moves(self, board : list[list[Piece]]):
        moves = []
        if board[self.position[0] + self.direction][self.position[1]].color == "Neutral":
            moves.append((self.position[0] + self.direction, self.position[1]))
        if self.has_moved is False and board[self.position[0] + self.direction * 2][self.position[1]].color == "Neutral" and board[self.position[0] + self.direction][self.position[1]].color == "Neutral":
            moves.append((self.position[0] + 2*self.direction, self.position[1]))
        if self.position[1] + 1 in range(8) and board[self.position[0] + self.direction][self.position[1] + 1].color == self.opposite_color:
            moves.append((self.position[0] + self.direction, self.position[1] + 1))
        if self.position[1] - 1 in range(8) and board[self.position[0] + self.direction][self.position[1] - 1].color == self.opposite_color:
            moves.append((self.position[0] + self.direction, self.position[1] - 1))
        return moves

    def copy(self):
        new_pawn = Pawn(self.color, self.position)
        new_pawn.has_moved = self.has_moved
        return new_pawn

class Rook(Piece):
    def __init__(self, color : str, position : tuple) -> None:
        Piece.__init__(self, color, position, "images/" + color + "_rook.png")

    def possible_moves(self, board : list[list[Piece]]):
        moves = []
        for i in range(1, 8):
            if self.position[0] + i not in range(8) or board[self.position[0] + i][self.position[1]].color == self.color:
                break
            if board[self.position[0] + i][self.position[1]].color == self.opposite_color:
                moves.append((self.position[0] + i, self.position[1]))
                break
            moves.append((self.position[0] + i, self.position[1]))
        for i in range(1, 8):
            if self.position[0] - i not in range(8) or board[self.position[0] - i][self.position[1]].color == self.color:
                break
            if board[self.position[0] - i][self.position[1]].color == self.opposite_color:
                moves.append((self.position[0] - i, self.position[1]))
                break
            moves.append((self.position[0] - i, self.position[1]))
        for i in range(1, 8):
            if self.position[1] + i not in range(8) or board[self.position[0]][self.position[1] + i].color == self.color:
                break
            if board[self.position[0]][self.position[1] + i].color == self.opposite_color:
                moves.append((self.position[0], self.position[1] + i))
                break
            moves.append((self.position[0], self.position[1] + i))
        for i in range(1, 8):
            if self.position[1] - i not in range(8) or board[self.position[0]][self.position[1] - i].color == self.color:
                break
            if board[self.position[0]][self.position[1] - i].color == self.opposite_color:
                moves.append((self.position[0], self.position[1] - i))
                break
            moves.append((self.position[0], self.position[1] - i))
        return moves

    def copy(self):
        new_rook = Rook(self.color, self.position)
        new_rook.has_moved = self.has_moved
        return new_rook


class Knight(Piece):
    def __init__(self, color : str, position : tuple) -> None:
        Piece.__init__(self, color, position, "images/" + color + "_knight.png")

    def possible_moves(self, board : list[list[Piece]]):
        moves = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                if abs(i) + abs(j) == 3 and self.position[0] + i in range(8) and self.position[1] + j in range(8):
                    if board[self.position[0] + i][self.position[1] + j].color != self.color:
                        moves.append((self.position[0] + i, self.position[1] + j))
        return moves

    def copy(self):
        return Knight(self.color, self.position)


class Bishop(Piece):
    def __init__(self, color : str, position : tuple) -> None:
        Piece.__init__(self, color, position, "images/" + color + "_bishop.png")

    def possible_moves(self, board : list[list[Piece]]):
        moves = []
        for i in range(1, 8):
            if self.position[0] + i not in range(8) or self.position[1] + i not in range(8) or board[self.position[0] + i][self.position[1] + i].color == self.color:
                break
            if board[self.position[0] + i][self.position[1] + i].color == self.opposite_color:
                moves.append((self.position[0] + i, self.position[1] + i))
                break
            moves.append((self.position[0] + i, self.position[1] + i))
        for i in range(1, 8):
            if self.position[0] - i not in range(8) or self.position[1] - i not in range(8) or board[self.position[0] - i][self.position[1] - i].color == self.color:
                break
            if board[self.position[0] - i][self.position[1] - i].color == self.opposite_color:
                moves.append((self.position[0] - i, self.position[1] - i))
                break
            moves.append((self.position[0] - i, self.position[1] - i))
        for i in range(1, 8):
            if self.position[0] + i not in range(8) or self.position[1] - i not in range(8) or board[self.position[0] + i][self.position[1] - i].color == self.color:
                break
            if board[self.position[0] + i][self.position[1] - i].color == self.opposite_color:
                moves.append((self.position[0] + i, self.position[1] - i))
                break
            moves.append((self.position[0] + i, self.position[1] - i))
        for i in range(1, 8):
            if self.position[0] - i not in range(8) or self.position[1] + i not in range(8) or board[self.position[0] - i][self.position[1] + i].color == self.color:
                break
            if board[self.position[0] - i][self.position[1] + i].color == self.opposite_color:
                moves.append((self.position[0] - i, self.position[1] + i))
                break
            moves.append((self.position[0] - i, self.position[1] + i))
        return moves

    def copy(self):
        new_bishop = Bishop(self.color, self.position)
        new_bishop.has_moved = self.has_moved
        return new_bishop

class Queen(Piece):
    def __init__(self, color : str, position : tuple) -> None:
        Piece.__init__(self, color, position, "images/" + color + "_queen.png")

    def possible_moves(self, board : list[list[Piece]]):
        moves = []
        for i in range(1, 8):
            if self.position[0] + i not in range(8) or board[self.position[0] + i][self.position[1]].color == self.color:
                break
            if board[self.position[0] + i][self.position[1]].color == self.opposite_color:
                moves.append((self.position[0] + i, self.position[1]))
                break
            moves.append((self.position[0] + i, self.position[1]))
        for i in range(1, 8):
            if self.position[0] - i not in range(8) or board[self.position[0] - i][self.position[1]].color == self.color:
                break
            if board[self.position[0] - i][self.position[1]].color == self.opposite_color:
                moves.append((self.position[0] - i, self.position[1]))
                break
            moves.append((self.position[0] - i, self.position[1]))
        for i in range(1, 8):
            if self.position[1] + i not in range(8) or board[self.position[0]][self.position[1] + i].color == self.color:
                break
            if board[self.position[0]][self.position[1] + i].color == self.opposite_color:
                moves.append((self.position[0], self.position[1] + i))
                break
            moves.append((self.position[0], self.position[1] + i))
        for i in range(1, 8):
            if self.position[1] - i not in range(8) or board[self.position[0]][self.position[1] - i].color == self.color:
                break
            if board[self.position[0]][self.position[1] - i].color == self.opposite_color:
                moves.append((self.position[0], self.position[1] - i))
                break
            moves.append((self.position[0], self.position[1] - i))
        for i in range(1, 8):
            if self.position[0] + i not in range(8) or self.position[1] + i not in range(8) or board[self.position[0] + i][self.position[1] + i].color == self.color:
                break
            if board[self.position[0] + i][self.position[1] + i].color == self.opposite_color:
                moves.append((self.position[0] + i, self.position[1] + i))
                break
            moves.append((self.position[0] + i, self.position[1] + i))
        for i in range(1, 8):
            if self.position[0] - i not in range(8) or self.position[1] - i not in range(8) or board[self.position[0] - i][self.position[1] - i].color == self.color:
                break
            if board[self.position[0] - i][self.position[1] - i].color == self.opposite_color:
                moves.append((self.position[0] - i, self.position[1] - i))
                break
            moves.append((self.position[0] - i, self.position[1] - i))
        for i in range(1, 8):
            if self.position[0] + i not in range(8) or self.position[1] - i not in range(8) or board[self.position[0] + i][self.position[1] - i].color == self.color:
                break
            if board[self.position[0] + i][self.position[1] - i].color == self.opposite_color:
                moves.append((self.position[0] + i, self.position[1] - i))
                break
            moves.append((self.position[0] + i, self.position[1] - i))
        for i in range(1, 8):
            if self.position[0] - i not in range(8) or self.position[1] + i not in range(8) or board[self.position[0] - i][self.position[1] + i].color == self.color:
                break
            if board[self.position[0] - i][self.position[1] + i].color == self.opposite_color:
                moves.append((self.position[0] - i, self.position[1] + i))
                break
            moves.append((self.position[0] - i, self.position[1] + i))
        return moves

    def copy(self):
        new_queen = Queen(self.color, self.position)
        new_queen.has_moved = self.has_moved
        return new_queen

class King(Piece):
    def __init__(self, color : str, position : tuple) -> None:
        Piece.__init__(self, color, position, "images/" + color + "_king.png")

    def possible_moves(self, board : list[list[Piece]]):
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if self.position[0] + i in range(8) and self.position[1] + j in range(8) and board[self.position[0] + i][self.position[1] + j].color != self.color:
                    moves.append((self.position[0] + i, self.position[1] + j))

        return moves

    def copy(self):
        new_king = King(self.color, self.position)
        new_king.has_moved = self.has_moved
        return new_king
