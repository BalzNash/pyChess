import pygame

pygame.init()
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Chess Game")
font = pygame.font.Font(None, 30)
clock = pygame.time.Clock()

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
        self.x = row * width
        self.y = col * width
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


class Piece:
    def __init__(self, square_num, color):
        self.position = square_num
        self.color = color
    
class Pawn(Piece):
    def __init__(self, square_num, color):
        super().__init__(square_num, color)
        self.type = 'pawn'
        self.color = 'color'
        self.has_moved = False

    def move(self, new_square):
        if new_square in self.get_moves():
            self.position = new_square

    def get_valid_moves(self, flat_grid):
        candidates = [max(0, self.position - 8)]
        if not self.has_moved:
            candidates.append(max(0, self.position - 16))
        return [move for move in candidates if not flat_grid[move-1].piece]



def make_grid(rows, width):
    grid = []
    gap = width // rows
    colors = [(128,128,128), (255,255,255)]
    color_idx = 0
    for i in range(rows):
        color_idx += 1
        grid.append([])
        for j in range(rows):
            spot = Square(j, i, gap, colors[color_idx % 2])
            grid[i].append(spot)
            color_idx += 1

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


def draw(win, grid, pawn, fps):
    win.fill(WHITE)


    for row in grid:
        for square in row:
            square.draw(win)
            if square.piece:
                win.blit(pawn, (square.x -17, square.y -40))
    if fps:
        win.blit(fps, (2, 2))
    
    pygame.display.update()


def main(win, width):
    ROWS = 8
    grid = make_grid(ROWS, width)
    flat_grid = [item for sublist in grid for item in sublist]
    create_pieces(grid)
    pawn = pygame.image.load("pawn4.png")
    pawn = pygame.transform.scale(pawn, (130, 130))

    draw(win, grid, pawn, fps= "")
    
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
        
        fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))


        draw(win, grid, pawn,fps)

    
    pygame.quit()

main(WIN, WIDTH)