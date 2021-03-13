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

    def __init__(self, row, col, width, total_rows, color):
        self.num = Square.square_num
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = color
        self.width = width
        self.total_rows = total_rows
        Square.square_num += 1

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))



def make_grid(rows, width):
    grid = []
    gap = width // rows
    colors = [(128,128,128), (255,255,255)]
    color_idx = 0
    for i in range(rows):
        color_idx += 1
        grid.append([])
        for j in range(rows):
            spot = Square(i, j, gap, rows, colors[color_idx % 2])
            grid[i].append(spot)
            color_idx += 1

    return grid


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for square in row:
            square.draw(win)

    pygame.display.update()


def main(win, width):
    ROWS = 8
    grid = make_grid(ROWS, width)

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
    pygame.quit()

main(WIN, WIDTH)