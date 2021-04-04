import pygame
import os
#print(os.path.dirname(os.path.abspath(__file__)))


class Piece:
    def __init__(self, square_num, color):
        self.position = square_num
        self.color = color


class Pawn(Piece):
    def __init__(self, square_num, color):
        super().__init__(square_num, color)
        self.type = 'pawn'
        self.has_moved = False

    def get_valid_moves(self, flat_grid):
        if self.color == 'white':
            candidates = [self.position -8] if self.position -8 >= 1 else []
            if not self.has_moved:
                candidates.append(max(0, self.position -16)) if not flat_grid[self.position-8-1].piece else ""
            capture_candicates = [i for i in [self.position -9, self.position -7] if i >= 1]
            capture = [i for i in capture_candicates if flat_grid[i-1].piece and flat_grid[i-1].piece.color == 'black'] # FIX LIMIT
        
        else:
            candidates = [self.position +8] if self.position +8 <= 64 else []
            if not self.has_moved:
                candidates.append(max(0, self.position +16)) if not flat_grid[self.position+8-1].piece else ""
            capture_candicates = [i for i in [self.position +9, self.position +7] if i <= 64]
            capture = [i for i in capture_candicates if flat_grid[i-1].piece and flat_grid[i-1].piece.color == 'white'] # FIX LIMIT
        
        candidates = [move for move in candidates if not flat_grid[move-1].piece]

        if capture:
            candidates.extend(capture)

        return candidates
        


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
        
    def get_valid_moves(self, flat_grid):
        if self.color == 'white':
            candidates = rows_squares[flat_grid[self.position-1].row] + cols_squares[flat_grid[self.position-1].col]
            return [move for move in candidates if move != self.position and (flat_grid[move-1].piece == '' or flat_grid[move-1].piece.color == 'black')]
        else:
            candidates = rows_squares[flat_grid[self.position-1].row] + cols_squares[flat_grid[self.position-1].col]
            return [move for move in candidates if move != self.position and (flat_grid[move-1].piece == '' or flat_grid[move-1].piece.color == 'white')]


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

sprites_path = ".\data\\sprites\\"

queen = pygame.image.load(sprites_path + "01.png"), pygame.image.load(sprites_path + "11.png") 
queen = pygame.transform.scale(queen[0], (80, 80)), pygame.transform.scale(queen[1], (80, 80))

king = pygame.image.load(sprites_path + "02.png"), pygame.image.load(sprites_path + "12.png") 
king = pygame.transform.scale(king[0], (80, 80)), pygame.transform.scale(king[1], (80, 80))

knight = pygame.image.load(sprites_path + "03.png"), pygame.image.load(sprites_path + "13.png") 
knight = pygame.transform.scale(knight[0], (80, 80)), pygame.transform.scale(knight[1], (80, 80))

bishop = pygame.image.load(sprites_path + "04.png"), pygame.image.load(sprites_path + "14.png") 
bishop = pygame.transform.scale(bishop[0], (80, 80)), pygame.transform.scale(bishop[1], (80, 80))

rook = pygame.image.load(sprites_path + "05.png"), pygame.image.load( sprites_path +"15.png") 
rook = pygame.transform.scale(rook[0], (80, 80)), pygame.transform.scale(rook[1], (80, 80))

pawn = pygame.image.load(sprites_path + "06.png"), pygame.image.load(sprites_path + "16.png") 
pawn = pygame.transform.scale(pawn[0], (80, 80)), pygame.transform.scale(pawn[1], (80, 80))



#rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR

def FEN_converter(fen_position):
    pieces = []
    for char in fen_position:
        if char.isnumeric():
            for i in range(int(char)):
                pieces.append("")
        elif char == '/':
            pass
        else:
            pieces.append(char)
    return pieces


piece_mapper = {'p': Pawn, 'n': Knight, 'b': Bishop, 'r': Rook, 'q': Queen, 'k': King, 'P': Pawn, 'N': Knight, 'B': Bishop, 'R': Rook, 'Q': Queen, 'K': King}

sprite_mapper = {'pawn': pawn, 'knight': knight, 'bishop': bishop, 'rook': rook, 'queen': queen, 'king': king}

rows_squares = {0: [1,2,3,4,5,6,7,8],
                1: [9,10,11,12,13,14,15,16],
                2: [17,18,19,20,21,22,23,24],
                3: [25,26,27,28,29,30,31,32],
                4: [33,34,35,36,37,38,39,40],
                5: [41,42,43,44,45,46,47,48],
                6: [49,50,51,52,53,54,55,56],
                7: [57,58,59,60,61,62,63,64]}

cols_squares = {0: [1,9,17,25,33,41,49,57],
                1: [2,10,18,26,34,42,50,58],
                2: [3,11,19,27,35,43,51,59],
                3: [4,12,20,28,36,44,52,60],
                4: [5,13,21,29,37,45,53,61],
                5: [6,14,22,30,38,46,54,62],
                6: [7,15,23,31,39,47,55,63],
                7: [8,16,24,32,40,48,56,64]}