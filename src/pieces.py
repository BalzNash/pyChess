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
            candidates = [max(0, self.position -8)]
            if not self.has_moved:
                candidates.append(max(0, self.position -16))
            capture = [i for i in [self.position -9, self.position -7] if flat_grid[i-1].piece and flat_grid[i-1].piece.color == 'black'] # FIX LIMIT, NOW IT GOES BELOW SQUARE 0
        
        else:
            candidates = [max(0, self.position +8)]
            if not self.has_moved:
                candidates.append(max(0, self.position +16))
            capture = [i for i in [self.position +9, self.position +7] if flat_grid[i-1].piece and flat_grid[i-1].piece.color == 'white'] # FIX LIMIT, NOW IT GOES PAST SQUARE 64
        
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