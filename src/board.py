import pygame

RED = (255, 0, 0)
BOARD_1 = (232, 231, 201)
BOARD_2 = (90, 135, 113)

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

    def highlight_square(self):
        self.color = RED

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def set_default_color(self):
        self.color = self.default_color


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