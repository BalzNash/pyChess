import pygame

RED = (255, 0, 0)

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

    def color_square(self):
        self.color = RED

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))