import random
import time

import pygame
from pygame._sdl2 import Window


def initialize_board():
    # Создаем пустое поле 4x4
    return [[0] * 4 for _ in range(4)]


def add_new_tile(board):
    empty_positions = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if board[i][j] == 0]
    if empty_positions:
        i, j = random.choice(empty_positions)
        new_tile_value = random.choices((2, 4), weights=[0.8, 0.2])[0]
        board[i][j] = new_tile_value


def move(board, direction):
    # Перемещение плиток в указанном направлении
    new_board = [row.copy() for row in board]

    if direction == 'left':
        for i in range(4):
            new_board[i] = merge(new_board[i])
    elif direction == 'right':
        for i in range(4):
            new_board[i] = merge(new_board[i][::-1])[::-1]
    elif direction == 'up':
        for j in range(4):
            column = [new_board[i][j] for i in range(4)]
            merged_column = merge(column)
            for i in range(4):
                new_board[i][j] = merged_column[i]
    elif direction == 'down':
        for j in range(4):
            column = [new_board[i][j] for i in range(4)][::-1]
            merged_column = merge(column)[::-1]
            for i in range(4):
                new_board[i][j] = merged_column[i]

    return new_board


def merge(line):
    # Слияние плиток в линии
    result = [0] * 4
    merged = [False] * 4
    index = 0

    for i in range(4):
        if line[i] != 0:
            if index > 0 and line[i] == result[index - 1] and not merged[index - 1]:
                # Объединяем две одинаковые плитки
                result[index - 1] *= 2
                merged[index - 1] = True
            else:
                # Перемещаем плитку в новую позицию
                result[index] = line[i]
                index += 1

    return result


def draw_board():
    pygame.draw.rect(screen, GRID_COLOR, (-10, 0, WIDTH + 20, HEIGHT + 25), 10)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            tile_value = board[i][j]
            tile_color = TILE_COLORS.get(tile_value, TILE_COLORS[0])
            pygame.draw.rect(screen, tile_color,
                             (j * TILE_SIZE + 10, i * TILE_SIZE + 55, TILE_SIZE - 20, TILE_SIZE - 20))
            if tile_value != 0:
                font = pygame.font.Font(None, 36)
                text = font.render(str(tile_value), True, (0, 0, 0))
                text_rect = text.get_rect(
                    center=(j * TILE_SIZE + TILE_SIZE // 2, (i * TILE_SIZE + TILE_SIZE // 2) + 35))
                screen.blit(text, text_rect)


def can_move(board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE - 1):
            if board[i][j] == 0 or board[i][j] == board[i][j + 1]:
                return True

    for j in range(GRID_SIZE):
        for i in range(GRID_SIZE - 1):
            if board[i][j] == 0 or board[i][j] == board[i + 1][j]:
                return True

    return False


def check_win(board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == 2048:
                return True
    return False


def start_new_game():
    global board
    board = initialize_board()
    add_new_tile(board)
    add_new_tile(board)


def game_scene():
    global score, increment, x, y, x_, y_, window, board
    running = True
    moving = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Проверка на захват окна и выход
                if event.button == 1:
                    x_, y_ = event.pos
                    if WIDTH - 35 < x_ < WIDTH - 5 and 5 < y_ < 40:
                        time.sleep(0.1)
                        running = False
                        change_scene(None)
                    elif 5 < y_ < 40:
                        moving = True
            if event.type == pygame.MOUSEBUTTONUP:
                moving = False

            # Передвижение окна
            if event.type == pygame.MOUSEMOTION:
                if moving:
                    x += event.pos[0] - x_
                    y += event.pos[1] - y_
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_board = move(board, 'left')
                elif event.key == pygame.K_RIGHT:
                    new_board = move(board, 'right')
                elif event.key == pygame.K_UP:
                    new_board = move(board, 'up')
                elif event.key == pygame.K_DOWN:
                    new_board = move(board, 'down')

                if new_board != board:
                    board = new_board
                    add_new_tile(board)

                    if check_win(board):
                        running = False
                        change_scene(end_scene)

                    if not can_move(board):
                        running = False
                        change_scene(end_scene)

        draw_board()
        # Панель управления
        pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, WIDTH, 10))
        pygame.draw.rect(screen, (230, 5, 64), (0, 0, WIDTH, HEIGHT), 5, border_radius=5)
        pygame.draw.rect(screen, (230, 5, 64), (0, 35, WIDTH, 5))
        font = pygame.font.SysFont("arial", 27)
        font.set_bold(True)
        text = font.render("2 0 4 8", False, (230, 5, 64))
        screen.blit(text, (35, 5))
        pygame.draw.circle(screen, (230, 5, 64), (WIDTH - 20, 20), 11, 3)
        pygame.draw.polygon(screen, (230, 5, 64),
                            ((WIDTH - 27, 15), (WIDTH - 25, 13), (WIDTH - 13, 25), (WIDTH - 15, 27)))
        pygame.draw.polygon(screen, (230, 5, 64),
                            ((WIDTH - 13, 15), (WIDTH - 15, 13), (WIDTH - 27, 25), (WIDTH - 25, 27)))
        pygame.display.flip()
        window.position = (x, y)
        screen.fill(BACKGROUND_COLOR)


def end_scene():
    global score, increment, x, y, x_, y_, window
    running = True
    moving = False
    while running:
        screen.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont("arial", 27)
        font.set_bold(True)
        text = font.render("Игра окончена!", False, (230, 5, 64))
        text2 = font.render("Чтоб начать новую - нажмите R", False, (230, 5, 64))
        screen.blit(text, (125, HEIGHT // 3))
        screen.blit(text2, (40, HEIGHT // 3 + 45))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Проверка на захват окна и выход
                if event.button == 1:
                    x_, y_ = event.pos
                    if WIDTH - 35 < x_ < WIDTH - 5 and 5 < y_ < 40:
                        time.sleep(0.1)
                        running = False
                        change_scene(None)
                    elif 5 < y_ < 40:
                        moving = True
            if event.type == pygame.MOUSEBUTTONUP:
                moving = False

            # Передвижение окна
            if event.type == pygame.MOUSEMOTION:
                if moving:
                    x += event.pos[0] - x_
                    y += event.pos[1] - y_

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    start_new_game()
                    running = False
                    change_scene(game_scene)

        # Панель управления
        pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, WIDTH, 10))
        pygame.draw.rect(screen, (230, 5, 64), (0, 0, WIDTH, HEIGHT), 5, border_radius=5)
        pygame.draw.rect(screen, (230, 5, 64), (0, 35, WIDTH, 5))
        font = pygame.font.SysFont("arial", 27)
        font.set_bold(True)
        text = font.render("2 0 4 8", False, (230, 5, 64))
        screen.blit(text, (35, 5))
        pygame.draw.circle(screen, (230, 5, 64), (WIDTH - 20, 20), 11, 3)
        pygame.draw.polygon(screen, (230, 5, 64),
                            ((WIDTH - 27, 15), (WIDTH - 25, 13), (WIDTH - 13, 25), (WIDTH - 15, 27)))
        pygame.draw.polygon(screen, (230, 5, 64),
                            ((WIDTH - 13, 15), (WIDTH - 15, 13), (WIDTH - 27, 25), (WIDTH - 25, 27)))
        pygame.display.flip()
        window.position = (x, y)
        screen.fill(BACKGROUND_COLOR)


def change_scene(scene):
    global current_scene
    current_scene = scene


# Инициализация Pygame
pygame.init()

# Определение констант
WIDTH, HEIGHT = 400, 460
GRID_SIZE = 4
TILE_SIZE = WIDTH // GRID_SIZE

# Определение цветов
BACKGROUND_COLOR = (9, 5, 13)
GRID_COLOR = (24, 24, 36)
TILE_COLORS = {
    0: (24, 24, 36),
    2: (230, 5, 64),
    4: (230, 36, 88),
    8: (194, 40, 81),
    16: (168, 22, 61),
    32: (189, 0, 50),
    64: (168, 7, 50),
    128: (138, 26, 56),
    256: (125, 4, 36),
    512: (120, 12, 41),
    1024: (105, 9, 35),
    2048: (87, 9, 30)
}
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME, pygame.SCALED)
pygame.display.set_caption('2048 Game')
x_, y_ = 0, 0
x = pygame.display.Info().current_w / 2
y = pygame.display.Info().current_h / 8
window = Window.from_display_module()
start_new_game()
current_scene = game_scene

while current_scene is not None:
    current_scene()
