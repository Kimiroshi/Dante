import os
import sys
import time

import pygame
import random
from pygame._sdl2 import Window


def load_image(name, game, colorkey=None):
    fullname = os.path.join(f'data\\{game}', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def create_particles(position, particle_count, gravity, incr):
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers), gravity, incr)


def change_scene(scene):
    global current_scene
    current_scene = scene


def main_page():
    global score, increment, x, y, x_, y_, window
    moving = False
    running = True
    button = Button(160, 240.25, 65, 65, 'data/emoji_clicker/apple.png', 'data/emoji_clicker/button_click.wav')
    shop = Button(285, 50, 65, 65, 'data/emoji_clicker/shop.png', 'data/emoji_clicker/shop.wav')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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

                # Создаём частицы по щелчку мыши
                if event.button == 1 and button.is_hovered:
                    create_particles(pygame.mouse.get_pos(), 1, -0.05, increment)
                    score += int(increment)

                if event.button == 1 and shop.is_hovered:
                    change_scene(shop_page)
                    running = False

            if event.type == pygame.MOUSEBUTTONUP:
                moving = False

            # Передвижение окна
            if event.type == pygame.MOUSEMOTION:
                if moving:
                    x += event.pos[0] - x_
                    y += event.pos[1] - y_

            button.handle_event(event)
            shop.handle_event(event)
        window.position = (x, y)
        screen.fill((9, 5, 13))

        # Панель управления
        pygame.draw.rect(screen, (230, 5, 64), (0, 0, WIDTH, HEIGHT), 5, border_radius=5)
        pygame.draw.rect(screen, (230, 5, 64), (0, 35, WIDTH, 5))
        font = pygame.font.SysFont("arial", 27)
        font.set_bold(True)
        text = font.render("К л и к е р", False, (230, 5, 64))
        screen.blit(text, (35, 5))
        pygame.draw.circle(screen, (230, 5, 64), (WIDTH - 20, 20), 11, 3)
        pygame.draw.polygon(screen, (230, 5, 64),
                            ((WIDTH - 27, 15), (WIDTH - 25, 13), (WIDTH - 13, 25), (WIDTH - 15, 27)))
        pygame.draw.polygon(screen, (230, 5, 64),
                            ((WIDTH - 13, 15), (WIDTH - 15, 13), (WIDTH - 27, 25), (WIDTH - 25, 27)))

        # Кнопка кликера + Мышка
        button.check_hover(pygame.mouse.get_pos())
        button.draw(screen)
        shop.check_hover(pygame.mouse.get_pos())
        shop.draw(screen)
        if button.is_hovered or 5 < pygame.mouse.get_pos()[1] < 40 or shop.is_hovered:
            screen.blit(hover, pygame.mouse.get_pos())
        else:
            screen.blit(mouse, pygame.mouse.get_pos())

        # Счёт
        text = font.render(f"СЧЁТ: {score}", False, (230, 5, 64))
        screen.blit(text, (20, 60))

        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)


def shop_page():
    global score, increment, x, y, x_, y_, window
    moving = False

    running = True
    door = Button(285, 50, 65, 65, 'data/emoji_clicker/door.png', 'data/emoji_clicker/door.wav')
    multiply = Button(20, 400, 65, 65, 'data/emoji_clicker/multiply.png', 'data/emoji_clicker/buy.wav')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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

                if event.button == 1 and door.is_hovered:
                    change_scene(main_page)
                    running = False

                if event.button == 1 and multiply.is_hovered:
                    if int(increment) * 2 <= 32 and score >= all_prices[increment]:
                        score -= all_prices[increment]
                        increment = str(int(increment) * 2)
                        multiply.handle_event(event)
                    else:
                        pass

            if event.type == pygame.MOUSEBUTTONUP:
                moving = False

            # Передвижение окна
            if event.type == pygame.MOUSEMOTION:
                if moving:
                    x += event.pos[0] - x_
                    y += event.pos[1] - y_

            door.handle_event(event)
        window.position = (x, y)
        screen.fill((9, 5, 13))

        # Панель управления
        pygame.draw.rect(screen, (230, 5, 64), (0, 0, WIDTH, HEIGHT), 5, border_radius=5)
        pygame.draw.rect(screen, (230, 5, 64), (0, 35, WIDTH, 5))
        font = pygame.font.SysFont("arial", 27)
        font.set_bold(True)
        text = font.render("К л и к е р", False, (230, 5, 64))
        screen.blit(text, (35, 5))
        pygame.draw.circle(screen, (230, 5, 64), (WIDTH - 20, 20), 11, 3)
        pygame.draw.polygon(screen, (230, 5, 64),
                            ((WIDTH - 27, 15), (WIDTH - 25, 13), (WIDTH - 13, 25), (WIDTH - 15, 27)))
        pygame.draw.polygon(screen, (230, 5, 64),
                            ((WIDTH - 13, 15), (WIDTH - 15, 13), (WIDTH - 27, 25), (WIDTH - 25, 27)))

        # Кнопка кликера + Мышка
        door.check_hover(pygame.mouse.get_pos())
        door.draw(screen)
        multiply.check_hover(pygame.mouse.get_pos())
        multiply.draw(screen)
        if 5 < pygame.mouse.get_pos()[1] < 40 or door.is_hovered or multiply.is_hovered:
            screen.blit(hover, pygame.mouse.get_pos())
        else:
            screen.blit(mouse, pygame.mouse.get_pos())

        # Счёт
        text = font.render(f"СЧЁТ: {score}", False, (230, 5, 64))
        screen.blit(text, (20, 60))
        text = font.render(' -- УМНОЖИТЬ КЛИКИ', False, (230, 5, 64))
        screen.blit(text, (85, 420))
        lvls = ('1', '2', '4', '8', '16')
        text = font.render(f'LVL: {lvls.index(increment) + 1 if increment != "32" else 6}', False, (230, 5, 64))
        screen.blit(text, (85, 480))
        if increment != '32':
            text = font.render(f'ЦЕНА: {all_prices[increment]}', False, (230, 5, 64))
        else:
            text = font.render(f'ЦЕНА: ∞', False, (230, 5, 64))
        screen.blit(text, (85, 450))

        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)


WIDTH = 380
HEIGHT = 625
current_scene = main_page
screen_rect = (0, 90, WIDTH, HEIGHT)
size = (WIDTH, HEIGHT)

mouse = load_image('mouse.png', 'emoji_clicker')
mouse = pygame.transform.scale(mouse, (48, 48))
hover = load_image('mouse_hover.png', 'emoji_clicker')
hover = pygame.transform.scale(hover, (48, 48))

all_sprites = pygame.sprite.Group()
button_group = pygame.sprite.Group()


class Button:
    def __init__(self, x, y, w, h, img, sound):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = pygame.mixer.Sound(sound)
        self.sound.set_volume(0.30)
        self.is_hovered = False

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy, gravity, incr):
        super().__init__(all_sprites)
        self.fire = [pygame.transform.scale(load_image(f"{incr}.png", 'emoji_clicker'), (50, 50))]
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = gravity

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('ну и зачем было сюда лезть?')
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode(size, pygame.NOFRAME, pygame.SCALED)
    clock = pygame.time.Clock()
    x_, y_ = 0, 0
    x = pygame.display.Info().current_w / 2
    y = pygame.display.Info().current_h / 8
    window = Window.from_display_module()
    score = 0
    all_prices = {'1': 100, '2': 400, '4': 1250, '8': 10000, '16': 65536}
    increment = '1'
    while current_scene is not None:
        current_scene()
