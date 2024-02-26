import pygame
from pygame._sdl2 import Window
import time
import os
import random


def generate_maze(width, height):
    maze_width = width * 2 + 1
    maze_height = height * 2 + 1
    maze = [['2' for _ in range(maze_width)] for _ in range(maze_height)]
    start_x = random.randint(0, width - 1) * 2 + 1
    start_y = random.randint(0, height - 1) * 2 + 1
    maze[start_y][start_x] = '1'
    stack = [(start_x, start_y)]
    while stack:
        x, y = stack[-1]
        maze[y][x] = '1'
        neighbors = []
        if x > 1:
            neighbors.append((x - 2, y))
        if x < maze_width - 2:
            neighbors.append((x + 2, y))
        if y > 1:
            neighbors.append((x, y - 2))
        if y < maze_height - 2:
            neighbors.append((x, y + 2))
        unvisited_neighbors = []
        for nx, ny in neighbors:
            if maze[ny][nx] == '2':
                unvisited_neighbors.append((nx, ny))
        if unvisited_neighbors:
            nx, ny = random.choice(unvisited_neighbors)
            maze[ny][nx] = '1'
            maze[ny + (y - ny) // 2][nx + (x - nx) // 2] = '1'
            stack.append((nx, ny))
        else:
            stack.pop()
    exit_x = random.choice(range(1, maze_width - 1, 2))
    maze[0][exit_x] = "3"
    out = []
    for i in range(len(maze[-2])):
        if maze[-2][i] == "1":
            out.append(i)
    maze[-1][random.choice(out)] = "4"
    return maze


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        fullname = os.path.join('data/data_maze', "coin.png")
        self.image = pygame.image.load(fullname)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Grass(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        fullname = os.path.join('data/data_maze', "grass.png")
        self.image = pygame.image.load(fullname)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        fullname = os.path.join('data/data_maze', "box.png")
        self.image = pygame.image.load(fullname)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Mar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        fullname = os.path.join('data/data_maze', "mar.png")
        self.image = pygame.image.load(fullname)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Mario:
    def __init__(self, board):
        self.width = len(board[0])
        self.height = len(board)
        self.board = board
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        board_group = pygame.sprite.Group()
        for i in range(self.height):
            for n in range(self.width):
                if self.board[i][n] == 1:
                    board_group.add(Grass(self.left + self.cell_size * n, self.top + self.cell_size * i))
                elif self.board[i][n] == 2:
                    board_group.add(Box(self.left + self.cell_size * n, self.top + self.cell_size * i))
                elif self.board[i][n] == 3:
                    board_group.add(Grass(self.left + self.cell_size * n, self.top + self.cell_size * i))
                    board_group.add(Mar(self.left + self.cell_size * n + 13, self.top + self.cell_size * i + 5))
                elif self.board[i][n] == 4:
                    board_group.add(Grass(self.left + self.cell_size * n, self.top + self.cell_size * i))
                    board_group.add(Coin(self.left + self.cell_size * n, self.top + self.cell_size * i))
        return board_group

    def right_(self):
        global win
        for i in range(len(self.board)):
            for n in range(len(self.board[i])):
                if self.board[i][n] == 3:
                    mario_ = (i, n)
        if mario_[1] != len(self.board[0]) - 1:
            if self.board[mario_[0]][mario_[1] + 1] == 1:
                self.board[mario_[0]][mario_[1]] = 1
                self.board[mario_[0]][mario_[1] + 1] = 3
                self.left -= self.cell_size
            elif self.board[mario_[0]][mario_[1] + 1] == 4:
                self.board[mario_[0]][mario_[1]] = 1
                self.board[mario_[0]][mario_[1] + 1] = 3
                self.left -= self.cell_size
                win = True

    def left_(self):
        global win
        for i in range(len(self.board)):
            for n in range(len(self.board[i])):
                if self.board[i][n] == 3:
                    mario_ = (i, n)
        if mario_[1] != 0:
            if self.board[mario_[0]][mario_[1] - 1] == 1:
                self.board[mario_[0]][mario_[1]] = 1
                self.board[mario_[0]][mario_[1] - 1] = 3
                self.left += self.cell_size
            elif self.board[mario_[0]][mario_[1] - 1] == 4:
                self.board[mario_[0]][mario_[1]] = 1
                self.board[mario_[0]][mario_[1] - 1] = 3
                self.left += self.cell_size
                win = True

    def up_(self):
        global win
        for i in range(len(self.board)):
            for n in range(len(self.board[i])):
                if self.board[i][n] == 3:
                    mario_ = (i, n)
        if mario_[0] != 0:
            if self.board[mario_[0] - 1][mario_[1]] == 1:
                self.board[mario_[0]][mario_[1]] = 1
                self.board[mario_[0] - 1][mario_[1]] = 3
                self.top += self.cell_size
            elif self.board[mario_[0] - 1][mario_[1]] == 4:
                self.board[mario_[0]][mario_[1]] = 1
                self.board[mario_[0] - 1][mario_[1]] = 3
                self.top += self.cell_size
                win = True

    def down_(self):
        global win
        for i in range(len(self.board)):
            for n in range(len(self.board[i])):
                if self.board[i][n] == 3:
                    mario_ = (i, n)
        if mario_[0] != len(self.board) - 1:
            if self.board[mario_[0] + 1][mario_[1]] == 1:
                self.board[mario_[0]][mario_[1]] = 1
                self.board[mario_[0] + 1][mario_[1]] = 3
                self.top -= self.cell_size
            elif self.board[mario_[0] + 1][mario_[1]] == 4:
                self.board[mario_[0]][mario_[1]] = 1
                self.board[mario_[0] + 1][mario_[1]] = 3
                self.top -= self.cell_size
                win = True


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Лабиринт")
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size, pygame.NOFRAME)
    x = pygame.display.Info().current_w / 2
    y = pygame.display.Info().current_h / 8
    window = Window.from_display_module()
    maze = []
    steps = []
    running = True
    moving = False
    start = False
    win = False
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
                    if 160 < x_ < 380 and 270 < y_ < 330:
                        if not start or win:
                            time.sleep(0.1)
                            win = False
                            start = True
                            h = 10
                            w = 10
                            board = list(map(lambda x: list(map(int, x)), generate_maze(10, 10)))
                            for i in range(len(board)):
                                for n in range(len(board[i])):
                                    if board[i][n] == 3:
                                        mario_ = (i, n)
                            mario = Mario(board)
                            mario.set_view(50 * (4 - mario_[1]), 50 * (4 - mario_[0]), 50)
            if event.type == pygame.MOUSEBUTTONUP:
                moving = False
            if event.type == pygame.MOUSEMOTION:
                if moving:
                    x += event.pos[0] - x_
                    y += event.pos[1] - y_
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if start:
                        start = False
                    else:
                        running = False
                if start:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        mario.right_()
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        mario.left_()
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        mario.up_()
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        mario.down_()
        window.position = (x, y)
        screen.fill((9, 5, 13))
        pygame.draw.rect(screen, (230, 5, 64), (0, 0, width, height), 5, border_radius=5)
        pygame.draw.rect(screen, (230, 5, 64), (0, 35, width, 5))
        font = pygame.font.SysFont("arial", 27)
        font.set_bold(True)
        text = font.render("Л а б и р и н т", False, (230, 5, 64))
        screen.blit(text, (35, 2))
        pygame.draw.circle(screen, (230, 5, 64), (width - 20, 20), 11, 3)
        pygame.draw.polygon(screen, (230, 5, 64),
                            ((width - 27, 15), (width - 25, 13), (width - 13, 25), (width - 15, 27)))
        pygame.draw.polygon(screen, (230, 5, 64),
                            ((width - 13, 15), (width - 15, 13), (width - 27, 25), (width - 25, 27)))
        if start:
            mario.render().draw(screen)
            pygame.draw.rect(screen, (9, 5, 13), (0, 0, width, 35))
            pygame.draw.rect(screen, (230, 5, 64), (0, 0, width, height), 5, border_radius=5)
            pygame.draw.rect(screen, (230, 5, 64), (0, 35, width, 5))
            font = pygame.font.SysFont("arial", 27)
            font.set_bold(True)
            text = font.render("Л а б и р и н т", False, (230, 5, 64))
            screen.blit(text, (35, 2))
            pygame.draw.circle(screen, (230, 5, 64), (width - 20, 20), 11, 3)
            pygame.draw.polygon(screen, (230, 5, 64),
                                ((width - 27, 15), (width - 25, 13), (width - 13, 25), (width - 15, 27)))
            pygame.draw.polygon(screen, (230, 5, 64),
                                ((width - 13, 15), (width - 15, 13), (width - 27, 25), (width - 25, 27)))
            if win:
                font = pygame.font.SysFont("arial", 80)
                font.set_bold(True)
                text = font.render("Y O U   W I N", False, (230, 5, 64))
                screen.blit(text, (50, 150))
                pygame.draw.rect(screen, (230, 5, 64), (160, 270, 220, 60), 5, border_radius=30)
                font = pygame.font.SysFont("arial", 45)
                font.set_bold(True)
                text = font.render("СТАРТ", False, (230, 5, 64))
                screen.blit(text, (205, 273))
        else:
            font = pygame.font.SysFont("arial", 50)
            font.set_bold(True)
            text = font.render("Л а б и р и н т", False, (230, 5, 64))
            screen.blit(text, (130, 200))
            pygame.draw.rect(screen, (230, 5, 64), (160, 270, 220, 60), 5, border_radius=30)
            font = pygame.font.SysFont("arial", 45)
            font.set_bold(True)
            text = font.render("СТАРТ", False, (230, 5, 64))
            screen.blit(text, (205, 273))
        pygame.display.flip()
    pygame.quit()
