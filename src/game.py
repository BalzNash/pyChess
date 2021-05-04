import pygame
from board import *
from pieces import *

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
ROWS = 8
pygame.display.set_caption("Chess Game")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
BOARD_1 = (232, 231, 201)
BOARD_2 = (90, 135, 113)


#---------------------------------- GAME FUNCTIONS ---------------------------------------


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = x // gap 
    col = y // gap
    return row, col


def select_square(grid, ROWS, width):
    pos = pygame.mouse.get_pos()
    row, col = get_clicked_pos(pos, ROWS, width)
    return grid[row][col]


def has_valid_moves(square, flat_grid, grid_array):
    if square.piece.get_valid_moves(flat_grid, grid_array):
        return True
    else:
        return False


def is_valid_start(square, players, to_move_idx, flat_grid, grid_array):
    return (square.piece and square.piece.color == players[to_move_idx] and has_valid_moves(square, flat_grid, grid_array))


def is_valid_target(start, target, flat_grid, grid_array):
    return target.num in start.piece.get_valid_moves(flat_grid, grid_array)


def are_moves_available(flat_grid, grid_array, players, to_move_idx):
    for square in flat_grid:
        if square.piece and square.piece.color == players[to_move_idx]:
            valid_moves = square.piece.get_valid_moves(flat_grid, grid_array)
            if valid_moves:
                for move in valid_moves:
                    if is_king_safe(square, flat_grid[move-1], flat_grid, grid_array):
                        return True
    return False

def is_check(flat_grid, grid_array, players, to_move_idx):
    to_move = players[to_move_idx]
    to_move_next = players[(to_move_idx+1)%2]
    for square in flat_grid:
        if square.piece and square.piece.color == to_move and square.piece.type == 'king':
            king_coord = square.num
            break

    attacked = []

    for square in flat_grid:
        if square.piece and square.piece.color == to_move_next:
            attacked.extend(square.piece.get_valid_moves(flat_grid, grid_array))
    return king_coord in attacked



def is_checkmate(check_flag):
    return (not are_moves_available() and check_flag)


def is_stalemate(check_flag):
    return  (not are_moves_available() and not check_flag)


def move_piece(start, target):
    start.piece, target.piece = "", start.piece
    target.piece.position = target.num
    target.piece.has_moved = True


def draw(win, grid):
    win.fill(WHITE)
    for row in grid:
        for square in row:
            square.draw(win)
            if square.piece:
                draw_pieces(square, win)
    pygame.display.update()


#-------------------------------------- MAIN ----------------------------------------------

# to add function for check flag

def main(win, width, ROWS):
    grid = make_grid(ROWS, width)
    flat_grid = [item for sublist in grid for item in sublist]
    grid_array = np.arange(1,65).reshape((8,8))
    
    FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
    parsed_FEN = FEN_converter(FEN)
    create_pieces(grid, parsed_FEN, piece_mapper)

    draw(win, grid)
    
    state = 'base'
    players = ['white', 'black']
    to_move_idx = 0
    game_ended = False

    run = True
    while run:
        for event in pygame.event.get():
            if state == 'base':
                if not are_moves_available(flat_grid,grid_array,players,to_move_idx):
                    state = 'end'
                elif pygame.mouse.get_pressed()[0]: #LEFT
                    start_square = select_square(grid, ROWS, width)
                    if is_valid_start(start_square, players, to_move_idx, flat_grid, grid_array):
                        start_square.highlight_square()
                        state = 'move'

            elif state == 'move':
                if pygame.mouse.get_pressed()[2]: #RIGHT
                    state = 'base'
                    start_square.set_default_color()

                if pygame.mouse.get_pressed()[0]:
                    target_square = select_square(grid, ROWS, width)

                    if is_valid_target(start_square, target_square, flat_grid, grid_array) and is_king_safe(start_square, target_square, flat_grid, grid_array):
                        move_piece(start_square, target_square)
                        start_square.set_default_color()
                        to_move_idx = (to_move_idx + 1) % 2
                        state = 'base'
            
            elif state == 'end':
                if game_ended:
                    pass
                else:
                    game_ended = True
                    if is_check(flat_grid, grid_array, players, to_move_idx):
                        print('Checkmate!', players[(to_move_idx+1) % 2], 'has won')
                    else:
                        print('Stalemate!')

                    
            
            if event.type == pygame.QUIT:
                run = False
        
        draw(win, grid)

    pygame.quit()


main(WIN, WIDTH, ROWS)