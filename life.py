import pygame
from pygame._sdl2 import Window
import time


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * self.width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.width):
            for n in range(self.height):
                pygame.draw.rect(screen, "white", (self.left + self.cell_size * i, self.top + self.cell_size * n,
                                                   self.cell_size, self.cell_size), 1)
                if self.board[n][i] == 1:
                    pygame.draw.rect(screen, (230, 5, 64), (self.left + self.cell_size * i + 1,
                                                            self.top + self.cell_size * n + 1,
                                                            self.cell_size - 2, self.cell_size - 2))

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        mouse_pos = ((mouse_pos[0] - self.left) // self.cell_size, (mouse_pos[1] - self.top) // self.cell_size)
        return mouse_pos

    def on_click(self, cell_coords):
        if 0 <= cell_coords[0] <= self.width - 1 and 0 <= cell_coords[1] <= self.height - 1:
            self.board[cell_coords[1]][cell_coords[0]] = 1

    def next_move(self):
        board_l = [[0] * self.width for i in range(self.height)]

        for i in range(self.height):
            for n in range(self.width):
                c = 0
                if i != 0:
                    if n != 0:
                        c += self.board[i - 1][n - 1]
                    else:
                        c += self.board[i - 1][-1]
                    c += self.board[i - 1][n]
                    if n != self.width - 1:
                        c += self.board[i - 1][n + 1]
                    else:
                        c += self.board[i - 1][0]
                else:
                    if n != 0:
                        c += self.board[-1][n - 1]
                    else:
                        c += self.board[-1][-1]
                    c += self.board[-1][n]
                    if n != self.width - 1:
                        c += self.board[-1][n + 1]
                    else:
                        c += self.board[-1][0]
                if n != 0:
                    c += self.board[i][n - 1]
                else:
                    c += self.board[i][-1]
                if n != self.width - 1:
                    c += self.board[i][n + 1]
                else:
                    c += self.board[i][0]
                if i != self.height - 1:
                    if n != 0:
                        c += self.board[i + 1][n - 1]
                    else:
                        c += self.board[i + 1][-1]
                    c += self.board[i + 1][n]
                    if n != self.width - 1:
                        c += self.board[i + 1][n + 1]
                    else:
                        c += self.board[i + 1][0]
                else:
                    if n != 0:
                        c += self.board[0][n - 1]
                    else:
                        c += self.board[0][-1]
                    c += self.board[0][n]
                    if n != self.width - 1:
                        c += self.board[0][n + 1]
                    else:
                        c += self.board[0][0]
                if ((c == 2 or c == 3) and self.board[i][n] == 1) or (c == 3 and self.board[i][n] == 0):
                    board_l[i][n] = 1
        self.board = board_l


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Жизнь")
    size = width, height = 752, 787
    screen = pygame.display.set_mode(size, pygame.NOFRAME, pygame.SCALED)
    x = pygame.display.Info().current_w / 2
    y = pygame.display.Info().current_h / 8
    window = Window.from_display_module()

    board = Board(53, 53)
    board.set_view(5, 40, 14)
    running = True
    evo = False
    moving = False
    start = False
    c = 0
    c_ = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x_, y_ = event.pos
                    if width - 35 < x_ < width - 5 and 5 < y_ < 40:
                        time.sleep(0.1)
                        running = False
                    elif 5 < y_ < 40:
                        moving = True
                    if not evo:
                        if start:
                            board.get_click(event.pos)
                    if 290 < x_ < 490 and 420 < y_ < 470:
                        if not start:
                            time.sleep(0.1)
                            start = True

                if event.button == 3:
                    if start:
                        if evo:
                            evo = False
                        else:
                            evo = True
            if event.type == pygame.MOUSEBUTTONUP:
                moving = False
            if event.type == pygame.MOUSEMOTION:
                if moving:
                    x += event.pos[0] - x_
                    y += event.pos[1] - y_
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if evo:
                        evo = False
                    else:
                        evo = True
                if event.key == pygame.K_ESCAPE:
                    if start:
                        start = False
                    else:
                        running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    c_ -= 0.1
                elif event.button == 5:
                    c_ += 0.1
        if evo:
            c += c_
        if c > 100:
            board.next_move()
            c = 0
        window.position = (x, y)
        screen.fill((9, 5, 13))
        pygame.draw.rect(screen, (230, 5, 64), (0, 0, width, height), 5, border_radius=5)
        pygame.draw.rect(screen, (230, 5, 64), (0, 35, width, 5))
        font = pygame.font.SysFont("arial", 27)
        font.set_bold(True)
        text = font.render("Ж и з н ь", False, (230, 5, 64))
        screen.blit(text, (35, 5))
        pygame.draw.circle(screen, (230, 5, 64), (width - 20, 20), 11, 3)
        pygame.draw.polygon(screen, (230, 5, 64),
                            ((width - 27, 15), (width - 25, 13), (width - 13, 25), (width - 15, 27)))
        pygame.draw.polygon(screen, (230, 5, 64),
                            ((width - 13, 15), (width - 15, 13), (width - 27, 25), (width - 25, 27)))
        if start:
            board.render(screen)
        else:
            font = pygame.font.SysFont("arial", 100)
            font.set_bold(True)
            text = font.render("Ж и з н ь", False, (230, 5, 64))
            screen.blit(text, (220, 250))
            pygame.draw.rect(screen, (230, 5, 64), (290, 420, 200, 50), 5, border_radius=30)
            font = pygame.font.SysFont("arial", 45)
            font.set_bold(True)
            text = font.render("СТАРТ", False, (230, 5, 64))
            screen.blit(text, (325, 418))
        pygame.display.flip()
    pygame.quit()
