# client.py
import time
import pygame
import socket
import requests
import configparser
from pygame._sdl2 import Window


class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 80)
        self.speed = 5

    def move_paddle(self, action):
        if action == "up" and self.rect.top > 36:
            self.rect.move_ip(0, -self.speed)
        elif action == "down" and self.rect.bottom < 600:
            self.rect.move_ip(0, self.speed)


pygame.init()
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size, pygame.NOFRAME, pygame.SCALED)
screen.fill((9, 5, 13))
pygame.draw.rect(screen, (9, 5, 13), (0, 0, WIDTH, 10))
pygame.draw.rect(screen, (230, 5, 64), (0, 0, WIDTH, HEIGHT), 5, border_radius=5)
pygame.draw.rect(screen, (230, 5, 64), (0, 35, WIDTH, 5))
font = pygame.font.SysFont("arial", 27)
font.set_bold(True)
text = font.render("П и н г - п о н г", False, (230, 5, 64))
screen.blit(text, (35, 5))
text = font.render("О ж и д а н и е  2 - г о  и г р о к а...", False, (230, 5, 64))
screen.blit(text, (245, 240))
pygame.draw.circle(screen, (230, 5, 64), (WIDTH - 20, 20), 11, 3)
pygame.draw.polygon(screen, (230, 5, 64),
                    ((WIDTH - 27, 15), (WIDTH - 25, 13), (WIDTH - 13, 25), (WIDTH - 15, 27)))
pygame.draw.polygon(screen, (230, 5, 64),
                    ((WIDTH - 13, 15), (WIDTH - 15, 13), (WIDTH - 27, 25), (WIDTH - 25, 27)))
pygame.display.update()

port = requests.get('https://sab.purpleglass.ru/api/coordinator-api/v1/').json()['port']
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('95.163.25.189', port))

config = configparser.ConfigParser()
config.read('config.ini')

player_id = config['DEFAULT']['id']
client.sendall(player_id.encode())

player_number = int(client.recv(1024).decode())  # Получаем номер игрока
paddle = Paddle(50, 250) if player_number == 1 else Paddle(735, 250)

dx_, dy_ = 0, 0
dx = pygame.display.Info().current_w / 2
dy = pygame.display.Info().current_h / 8
window = Window.from_display_module()
moving = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Проверка на захват окна и выход
            if event.button == 1:
                dx_, dy_ = event.pos
                if WIDTH - 35 < dx_ < WIDTH - 5 and 5 < dy_ < 40:
                    time.sleep(0.1)
                    running = False
                    pygame.quit()
                elif 5 < dy_ < 40:
                    moving = True
        if event.type == pygame.MOUSEBUTTONUP:
            moving = False

        # Передвижение окна
        if event.type == pygame.MOUSEMOTION:
            if moving:
                dx += event.pos[0] - dx_
                dy += event.pos[1] - dy_

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        paddle.move_paddle("up")
    if keys[pygame.K_DOWN]:
        paddle.move_paddle("down")

    data = f"{paddle.rect.x},{paddle.rect.y}"
    client.sendall(data.encode())

    data = client.recv(1024).decode()
    x1, y1, x2, y2, ball_x, ball_y = map(int, data.split(','))

    # Панель управления
    screen.fill((9, 5, 13))
    pygame.draw.rect(screen, (9, 5, 13), (0, 0, WIDTH, 10))
    pygame.draw.rect(screen, (230, 5, 64), (0, 0, WIDTH, HEIGHT), 5, border_radius=5)
    pygame.draw.rect(screen, (230, 5, 64), (0, 35, WIDTH, 5))
    font = pygame.font.SysFont("arial", 27)
    font.set_bold(True)
    text = font.render("П и н г - п о н г", False, (230, 5, 64))
    screen.blit(text, (35, 5))
    pygame.draw.circle(screen, (230, 5, 64), (WIDTH - 20, 20), 11, 3)
    pygame.draw.polygon(screen, (230, 5, 64),
                        ((WIDTH - 27, 15), (WIDTH - 25, 13), (WIDTH - 13, 25), (WIDTH - 15, 27)))
    pygame.draw.polygon(screen, (230, 5, 64),
                        ((WIDTH - 13, 15), (WIDTH - 15, 13), (WIDTH - 27, 25), (WIDTH - 25, 27)))
    window.position = (dx, dy)
    pygame.draw.rect(screen, (230, 5, 64), paddle.rect)
    pygame.draw.rect(screen, (189, 0, 50),
                     pygame.Rect(x2, y2, 15, 80) if player_number == 1 else pygame.Rect(x1, y1, 15, 80))
    pygame.draw.rect(screen, (125, 4, 36), pygame.Rect(ball_x, ball_y, 15, 15))
    pygame.display.update()
    pygame.time.delay(10)