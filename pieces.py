
class Piece:
    def __init__(self, square_num, color):
        self.position = square_num
        self.color = color

    def move(self, new_square):
        if new_square in self.get_moves():
            self.position = new_square

    def get_valid_moves(self, flat_grid):
        if self.color == 'black':
            sign = -1
        else:
            sign = 1
        candidates = [max(0, self.position +8*sign)]
        if not self.has_moved:
            candidates.append(max(0, self.position +16*sign))
        return [move for move in candidates if not flat_grid[move-1].piece]


class Pawn(Piece):
    def __init__(self, square_num, color):
        super().__init__(square_num, color)
        self.type = 'pawn'
        self.has_moved = False


class Bishop(Piece):
    def __init__(self, square_num, color):
        super().__init__(square_num, color)
        self.type = 'bishop'
        self.has_moved = False


class Knight(Piece):
    def __init__(self, square_num, color):
        super().__init__(square_num, color)
        self.type = 'knight'
        self.has_moved = False


class Rook(Piece):
    def __init__(self, square_num, color):
        super().__init__(square_num, color)
        self.type = 'rook'
        self.has_moved = False


class Queen(Piece):
    def __init__(self, square_num, color):
        super().__init__(square_num, color)
        self.type = 'queen'
        self.has_moved = False


class King(Piece):
    def __init__(self, square_num, color):
        super().__init__(square_num, color)
        self.type = 'king'
        self.has_moved = False
