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

    def __init__(self, row, col, width, total_rows, color, default_color):
        self.num = Square.square_num
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = color
        self.width = width
        self.total_rows = total_rows
        self.piece = ""
        self.default_color = default_color
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
    
    def get_moves(self, square):
        moves = ""

        if self.color == 'WHITE':
            moves = [min(0, self.position - 8)]
        else:
            moves =[max(64, self.position + 8)]
        
        return moves

    def move(self, new_square):
        if new_square in self.get_moves():
            self.position = new_square

    def get_valid_moves(self, flat_grid):
        candidates = [max(0, self.position - 8)]
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
            spot = Square(j, i, gap, rows, colors[color_idx % 2], colors[color_idx % 2])
            grid[i].append(spot)
            color_idx += 1

    return grid


def create_pieces(grid):
    pieces = []
    for row in grid:
        for square in row:
            if square.num <= 16 or square.num >= 49:
                pieces.append(Pawn(square.num, 'black'))
                square.piece = 'pawn'
            else:
                pieces.append("")
    return pieces


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def draw(win, grid, rows, width, pieces, grid_coord, pawn):
    win.fill(WHITE)


    for row in grid:
        for square in row:
            square.draw(win)

    for piece in pieces:
        if piece:
            win.blit(pawn, (grid_coord[piece.position -1][0] -17, grid_coord[piece.position -1][1] -40))
    
    # pawn = pygame.image.load("pawn4.png")
    # pawn = pygame.transform.scale(pawn, (130, 130))
    # win.blit(pawn, (-20, -40))
    
    pygame.display.update()


def main(win, width):
    ROWS = 8
    grid = make_grid(ROWS, width)
    flat_grid = [item for sublist in grid for item in sublist]
    grid_coord = [(square.x,square.y) for square in flat_grid]
    pieces = create_pieces(grid)
    pawn = pygame.image.load("pawn4.png")
    pawn = pygame.transform.scale(pawn, (130, 130))

    draw(win, grid, ROWS, width, pieces, grid_coord, pawn)
    
    state = 'base'

    run = True
    while run:
        for event in pygame.event.get():
            if state == 'base':
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    starting_square = grid[col][row]
                    selected_piece = pieces[starting_square.num-1]
                    if selected_piece:
                        starting_square.select_square()
                        state = 'move'
            elif state == 'move':
                if pygame.mouse.get_pressed()[2]:
                    state = 'base'
                    starting_square.color = starting_square.default_color

                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    selected_square = grid[col][row]
                    print(selected_square.num)
                    if selected_square.num in selected_piece.get_valid_moves(flat_grid):
                        starting_square.piece = ""
                        selected_piece.position = selected_square.num
                        pieces[starting_square.num -1], pieces[selected_square.num -1] = pieces[selected_square.num -1], pieces[starting_square.num -1]
                        selected_square.select_square2()
                        starting_square.color = starting_square.default_color
                        state = 'base'



            if event.type == pygame.QUIT:
                run = False
        
        draw(win, grid, ROWS, width, pieces, grid_coord, pawn)

    
    pygame.quit()

main(WIN, WIDTH)