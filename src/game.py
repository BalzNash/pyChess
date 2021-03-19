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


def make_grid(rows, width):
    grid = []
    gap = width // rows
    colors = [GREY, WHITE]
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

    row = y // gap
    col = x // gap

    return row, col


def draw(win, grid, pawn):
    win.fill(WHITE)

    for row in grid:
        for square in row:
            square.draw(win)
            if square.piece:
                draw_pieces(square, win)
    
    pygame.display.update()


def main(win, width):
    ROWS = 8
    
    FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
    parsed_FEN = FEN_converter(FEN)

    grid = make_grid(ROWS, width)
    flat_grid = [item for sublist in grid for item in sublist]
    
    create_pieces(grid, parsed_FEN, piece_mapper)

    draw(win, grid, pawn)
    
    state = 'base'

    run = True
    while run:
        for event in pygame.event.get():
            if state == 'base':
                if pygame.mouse.get_pressed()[0]: #LEFT
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    starting_square = grid[col][row]
                    selected_piece = starting_square.piece
                    if selected_piece:
                        starting_square.color_square()
                        state = 'move'
            elif state == 'move':
                if pygame.mouse.get_pressed()[2]: #RIGHT
                    state = 'base'
                    starting_square.color = starting_square.default_color

                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    target_square = grid[col][row]
                    if target_square.num in selected_piece.get_valid_moves(flat_grid):
                        starting_square.piece, target_square.piece = "", starting_square.piece
                        target_square.piece.position = target_square.num
                        target_square.piece.has_moved = True
                        #target_square.select_square2()
                        starting_square.color = starting_square.default_color
                        state = 'base'
            

            if event.type == pygame.QUIT:
                run = False
        
        


        draw(win, grid, pawn)

    
    pygame.quit()

main(WIN, WIDTH)