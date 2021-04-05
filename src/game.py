import pygame
from board import *
from pieces import *

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
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


def make_grid(rows, width):
    grid = []
    gap = width // rows
    colors = [BOARD_2, BOARD_1]
    color_idx = 0
    for i in range(rows):
        color_idx += 1
        grid.append([])
        for j in range(rows):
            spot = Square(i, j, gap, colors[color_idx % 2])
            grid[i].append(spot)
            color_idx += 1
    return grid


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



def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = x // gap 
    col = y // gap


    return row, col


def draw(win, grid):
    win.fill(WHITE)

    for row in grid:
        for square in row:
            square.draw(win)
            if square.piece:
                draw_pieces(square, win)
    
    pygame.display.update()


#-------------------------------------- MAIN ----------------------------------------------


def main(win, width):
    ROWS = 8
    FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
    parsed_FEN = FEN_converter(FEN)

    grid = make_grid(ROWS, width)
    flat_grid = [item for sublist in grid for item in sublist]
    grid_array = np.arange(1,65).reshape((8,8))
    
    create_pieces(grid, parsed_FEN, piece_mapper)

    draw(win, grid)
    
    state = 'base'
    players = ['white', 'black']
    to_move_idx = 0

    run = True
    while run:
        for event in pygame.event.get():
            if state == 'base':
                if pygame.mouse.get_pressed()[0]: #LEFT
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    print(row, col)
                    starting_square = grid[row][col]
                    selected_piece = starting_square.piece
                    if selected_piece and selected_piece.color == players[to_move_idx]:
                        starting_square.color_square()
                        state = 'move'
            elif state == 'move':
                if pygame.mouse.get_pressed()[2]: #RIGHT
                    state = 'base'
                    starting_square.color = starting_square.default_color

                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    target_square = grid[row][col]

                    if target_square.num in selected_piece.get_valid_moves(flat_grid, grid_array):
                        starting_square.piece, target_square.piece = "", starting_square.piece
                        target_square.piece.position = target_square.num
                        target_square.piece.has_moved = True
                        starting_square.color = starting_square.default_color
                        
                        to_move_idx = (to_move_idx + 1) % 2
                        state = 'base'
            
            if event.type == pygame.QUIT:
                run = False
        
        draw(win, grid)

    pygame.quit()


main(WIN, WIDTH)