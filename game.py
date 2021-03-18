from pieces import *
import pygame

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


class Square:
    square_num = 1

    def __init__(self, row, col, width, color):
        self.num = Square.square_num
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.width = width
        self.piece = ""
        self.color = color
        self.default_color = color
        Square.square_num += 1

    def select_square(self):
        self.color = RED
    
    def select_square2(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


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
    print(grid[0][1].row, grid[0][1].col, grid[0][1].x)
    return grid


def create_pieces(grid):
    for row in grid:
        for square in row:
            if square.num <= 16 or square.num >= 49:
                square.piece = Pawn(square.num, 'black')


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
                win.blit(pawn, (square.x + 10, square.y + 10))
    
    pygame.display.update()


def main(win, width):
    ROWS = 8
    grid = make_grid(ROWS, width)
    flat_grid = [item for sublist in grid for item in sublist]
    create_pieces(grid)
    pawn = pygame.image.load("piece0.png")
    pawn = pygame.transform.scale(pawn, (80, 80))

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
                        starting_square.select_square()
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