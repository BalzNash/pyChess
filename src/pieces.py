import pygame
import os
import numpy as np
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


    def get_valid_moves(self, flat_grid, grid_array):
        if self.color == 'white':
            valid_moves = [self.position -8] if self.position -8 >= 1 else []
            if not self.has_moved:
                valid_moves.append(self.position -16) if not flat_grid[self.position-8-1].piece else ""

            capture_candicates = [i for i in [self.position -9, self.position -7] if i >= 1 and np.where(grid_array == self.position)[0][0] != np.where(grid_array == i)[0][0]]
            captures = [i for i in capture_candicates if flat_grid[i-1].piece and flat_grid[i-1].piece.color == 'black']
        
        else:
            valid_moves = [self.position +8] if self.position +8 <= 64 else []
            if not self.has_moved:
                valid_moves.append(self.position +16) if not flat_grid[self.position+8-1].piece else ""

            capture_candicates = [i for i in [self.position +9, self.position +7] if i <= 64 and np.where(grid_array == self.position)[0][0] != np.where(grid_array == i)[0][0]]
            captures = [i for i in capture_candicates if flat_grid[i-1].piece and flat_grid[i-1].piece.color == 'white']
        
        valid_moves = [move for move in valid_moves if not flat_grid[move-1].piece]

        if captures:
            valid_moves.extend(captures)

        return valid_moves
        


class Bishop(Piece):
    def __init__(self, square_num, color):
        super().__init__(square_num, color)
        self.type = 'bishop'
        self.has_moved = False
    
    def get_candidates(self, flat_grid, diagonal):
        candidates = []

        for i in list(diagonal.values()):
            if self.position in i:
                diagonal = i
                diag_idx = diagonal.index(self.position)
                break

        moving_idx = diag_idx
        direction = 'right'
        while direction:
            if direction == 'right':
                moving_idx += 1
                try:
                    square_num = diagonal[moving_idx]
                    if flat_grid[square_num-1].piece:
                        candidates.append(square_num)
                        moving_idx = diag_idx
                        direction = 'left'
                    else:
                        candidates.append(square_num)
                except IndexError:
                    moving_idx = diag_idx
                    direction = 'left'
            else:
                moving_idx -= 1
                if moving_idx >= 0:
                    square_num = diagonal[moving_idx]
                    if flat_grid[square_num-1].piece:
                        candidates.append(square_num)
                        direction = ""
                    else:
                        candidates.append(square_num)
                else:
                    direction = ""
            
        return candidates


    def get_valid_moves(self, flat_grid, grid_array):
        candidates = self.get_candidates(flat_grid, diagonal_1_squares) + self.get_candidates(flat_grid, diagonal_2_squares)
        if self.color == 'white':
            return [move for move in candidates if (flat_grid[move-1].piece == '' or flat_grid[move-1].piece.color == 'black')]
        else:
            return [move for move in candidates if (flat_grid[move-1].piece == '' or flat_grid[move-1].piece.color == 'white')]




class Knight(Piece):
    def __init__(self, square_num, color):
        super().__init__(square_num, color)
        self.type = 'knight'
        self.has_moved = False
    
    def get_valid_moves(self, flat_grid, grid_array):
        candidates = [self.position -15, self.position -6, self.position +10, self.position +17,
                      self.position +15, self.position +6, self.position -10, self.position -17]

        candidates = [i for i in candidates if 1 <= i <= 64 and abs(np.where(grid_array == self.position)[0][0] - np.where(grid_array == i)[0][0]) <= 2 \
                                                            and abs(np.where(grid_array == self.position)[1][0] - np.where(grid_array == i)[1][0]) <= 2]        
        if self.color == 'white':
            return [move for move in candidates if (flat_grid[move-1].piece == '' or flat_grid[move-1].piece.color == 'black')]
        else:
            return [move for move in candidates if (flat_grid[move-1].piece == '' or flat_grid[move-1].piece.color == 'white')]        


class Rook(Piece):
    def __init__(self, square_num, color):
        super().__init__(square_num, color)
        self.type = 'rook'
        self.has_moved = False

    def get_candidates(self, row_col, flat_grid):
        candidates = []
        row_idx = row_col.index(self.position)
        moving_idx = row_idx
        direction = 'up'
        while direction:
            if direction == 'up':
                moving_idx += 1
                try:
                    square_num = row_col[moving_idx]
                    if flat_grid[square_num-1].piece:
                        candidates.append(square_num)
                        moving_idx = row_idx
                        direction = 'down'
                    else:
                        candidates.append(square_num)
                except IndexError:
                    moving_idx = row_idx
                    direction = 'down'
            
            else:
                moving_idx -= 1
                if moving_idx >= 0:
                    square_num = row_col[moving_idx]
                    if flat_grid[square_num-1].piece:
                        candidates.append(row_col[moving_idx])
                        direction = ""
                    else:
                        candidates.append(row_col[moving_idx])
                else:
                    direction = ""
            
        return candidates

    def get_valid_moves(self, flat_grid, grid_array):
        candidates_row = rows_squares[flat_grid[self.position-1].row]
        candidates_col = cols_squares[flat_grid[self.position-1].col]
        candidates = self.get_candidates(candidates_row, flat_grid) + self.get_candidates(candidates_col, flat_grid)
        
        if self.color == 'white':
            return [move for move in candidates if (flat_grid[move-1].piece == '' or flat_grid[move-1].piece.color == 'black')]
        else:
            return [move for move in candidates if (flat_grid[move-1].piece == '' or flat_grid[move-1].piece.color == 'white')]


class Queen(Piece):
    def __init__(self, square_num, color):
        super().__init__(square_num, color)
        self.type = 'queen'
        self.has_moved = False


    def get_candidates_row_col(self, row_col, flat_grid):
        candidates = []
        row_idx = row_col.index(self.position)
        moving_idx = row_idx
        direction = 'up'
        while direction:
            if direction == 'up':
                moving_idx += 1
                try:
                    square_num = row_col[moving_idx]
                    if flat_grid[square_num-1].piece:
                        candidates.append(square_num)
                        moving_idx = row_idx
                        direction = 'down'
                    else:
                        candidates.append(square_num)
                except IndexError:
                    moving_idx = row_idx
                    direction = 'down'
            
            else:
                moving_idx -= 1
                if moving_idx >= 0:
                    square_num = row_col[moving_idx]
                    if flat_grid[square_num-1].piece:
                        candidates.append(row_col[moving_idx])
                        direction = ""
                    else:
                        candidates.append(row_col[moving_idx])
                else:
                    direction = ""
        
        return candidates


    def get_candidates_diag(self, flat_grid, diagonals):
        candidates = []

        for i in list(diagonals.values()):
            if self.position in i:
                diagonal = i
                diag_idx = diagonal.index(self.position)
                break

        moving_idx = diag_idx
        direction = 'right'
        while direction:
            if direction == 'right':
                moving_idx += 1
                try:
                    square_num = diagonal[moving_idx]
                    if flat_grid[square_num-1].piece:
                        candidates.append(square_num)
                        moving_idx = diag_idx
                        direction = 'left'
                    else:
                        candidates.append(square_num)
                except IndexError:
                    moving_idx = diag_idx
                    direction = 'left'
            else:
                moving_idx -= 1
                if moving_idx >= 0:
                    square_num = diagonal[moving_idx]
                    if flat_grid[square_num-1].piece:
                        candidates.append(square_num)
                        direction = ""
                    else:
                        candidates.append(square_num)
                else:
                    direction = ""
            
        return candidates    


    def get_valid_moves(self, flat_grid, grid_array):
        candidates_row = rows_squares[flat_grid[self.position-1].row]
        candidates_col = cols_squares[flat_grid[self.position-1].col]
        candidates = self.get_candidates_row_col(candidates_row, flat_grid)  + self.get_candidates_row_col(candidates_col, flat_grid)  \
                   + self.get_candidates_diag(flat_grid, diagonal_1_squares) + self.get_candidates_diag(flat_grid, diagonal_2_squares)

        if self.color == 'white':
            return [move for move in candidates if (flat_grid[move-1].piece == '' or flat_grid[move-1].piece.color == 'black')]
        else:
            return [move for move in candidates if (flat_grid[move-1].piece == '' or flat_grid[move-1].piece.color == 'white')]


class King(Piece):
    def __init__(self, square_num, color):
        super().__init__(square_num, color)
        self.type = 'king'
        self.has_moved = False
    
    def get_valid_moves(self, flat_grid, grid_array):
        candidates = [self.position + 1, self.position + 8, self.position - 1, self.position -8,
                      self.position - 9, self.position - 7, self.position + 9, self.position +7]

        candidates = [i for i in candidates if 1 <= i <= 64 and abs(np.where(grid_array == self.position)[0][0] - np.where(grid_array == i)[0][0]) <= 1 \
                                                      and abs(np.where(grid_array == self.position)[1][0] - np.where(grid_array == i)[1][0]) <= 1]

        if self.color == 'white':
            return [move for move in candidates if (flat_grid[move-1].piece == '' or flat_grid[move-1].piece.color == 'black')]
        else:
            return [move for move in candidates if (flat_grid[move-1].piece == '' or flat_grid[move-1].piece.color == 'white')]


#------------------------------------- LOAD PIECES ------------------------------------------------------

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


def create_pieces(grid, parsed_FEN, mapping):
    i = 0
    for row in grid:
        for square in row:
            char = parsed_FEN[i]
            if char:
                square.piece = mapping[char](square.num, 'black')
                if char.isupper():
                    square.piece.color = 'white'
            i += 1


def draw_pieces(square, win):
    if square.piece.color == 'white':
        win.blit(sprite_mapper[square.piece.type][0], (square.x + 10, square.y + 10))
    else:
        win.blit(sprite_mapper[square.piece.type][1], (square.x + 10, square.y + 10))


#---------------------------------------- UTILS ----------------------------------------------------------


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


piece_mapper =  {'p': Pawn, 'n': Knight, 'b': Bishop, 'r': Rook, 'q': Queen, 'k': King, 'P': Pawn, 'N': Knight, 'B': Bishop, 'R': Rook, 'Q': Queen, 'K': King}

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

diagonal_1_squares = {0: [1],
                      1: [2,9],
                      2: [3,10,17],
                      3: [4,11,18,25],
                      4: [5,12,19,26,33],
                      5: [6,13,20,27,34,41],
                      6: [7,14,21,28,35,42,49],
                      7: [8,15,22,29,36,43,50,57],
                      8: [16,23,30,37,44,51,58],
                      9: [24,31,38,45,52,59],
                     10: [32,39,46,53,60],
                     11: [40,47,54,61],
                     12: [48,55,62],
                     13: [56,63],
                     14: [64]}

diagonal_2_squares = {0: [8],
                      1: [7,16],
                      2: [6,15,24],
                      3: [5,14,23,32],
                      4: [4,13,22,31,40],
                      5: [3,12,21,30,39,48],
                      6: [2,11,20,29,38,47,56],
                      7: [1,10,19,28,37,46,55,64],
                      8: [9,18,27,36,45,54,63],
                      9: [17,26,35,44,53,62],
                     10: [25,34,43,52,61],
                     11: [33,42,51,60],
                     12: [41,50,59],
                     13: [49,58],
                     14: [57]}
