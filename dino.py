import os
import time
import pygame

from random import randint
from pygame._sdl2 import Window


class Pole(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        fullname = os.path.join('data/data_dino', "pole.png")
        self.image = pygame.image.load(fullname)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.rect.x == -2400:
            self.rect.x = 2400
        self.rect.x -= 5


class Spike(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        fullname = os.path.join('data/data_dino/spikes', image)
        self.image = pygame.image.load(fullname)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = -100

    def update(self):
        global game_over
        self.rect.x -= 5
        if pygame.sprite.collide_mask(self, dino):
            game_over = True


class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        fullname = os.path.join('data/data_dino', "dino1.png")
        self.image = pygame.image.load(fullname)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 352

    def update(self):
        global count, jump
        if count // 10 % 2 == 0:
            fullname = os.path.join('data/data_dino', "dino2.png")
            self.image = pygame.image.load(fullname)
            self.mask = pygame.mask.from_surface(self.image)
        else:
            fullname = os.path.join('data/data_dino', "dino3.png")
            self.image = pygame.image.load(fullname)
            self.mask = pygame.mask.from_surface(self.image)
        if jump:
            fullname = os.path.join('data/data_dino', "dino1.png")
            self.image = pygame.image.load(fullname)
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.y -= 50 * (count_j / 100)
            if self.rect.y >= 352:
                jump = False
                self.rect.y = 352

    def death(self):
        fullname = os.path.join('data/data_dino', "dino4.png")
        self.image = pygame.image.load(fullname)
        self.mask = pygame.mask.from_surface(self.image)


class NewGame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        fullname = os.path.join('data/data_dino', "new_game.png")
        self.image = pygame.image.load(fullname)
        self.rect = self.image.get_rect()
        self.rect.x = 700
        self.rect.y = 172


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Динозаврик")
    size = width, height = 752, 787
    screen = pygame.display.set_mode(size, pygame.NOFRAME)
    x = pygame.display.Info().current_w / 2
    y = pygame.display.Info().current_h / 8
    window = Window.from_display_module()
    count = 0
    count_j = 100
    running = True
    moving = False
    start = False
    jump = False
    tap_mouse = False
    tap_space = False
    game_over = False
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
                    elif start and not game_over:
                        tap_mouse = True
                    if 290 < x_ < 490 and 420 < y_ < 470:
                        if not start:
                            time.sleep(0.1)
                            start = True
                            game_over = False
                            jump = False
                            count = 0
                            count_j = 32
                            size = width, height = 1000, 500
                            screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
                            pygame.display.update()
                            spikes = pygame.sprite.Group()
                            spikes.add(Spike("spike_big1.png"))
                            spikes.add(Spike("spike_big2.png"))
                            spikes.add(Spike("spike_big4.png"))
                            spikes.add(Spike("spike_small1.png"))
                            spikes.add(Spike("spike_small2.png"))
                            spikes.add(Spike("spike_small3.png"))
                            dino = Dino()
                            poles = pygame.sprite.Group()
                            poles.add(Pole(0, 430))
                            poles.add(Pole(2400, 430))
                            new_game = NewGame()
                    if 700 < x_ < 772 and 172 < y_ < 236:
                        if start and game_over:
                            time.sleep(0.2)
                            game_over = False
                            jump = False
                            count = 0
                            count_j = 100
                            size = width, height = 1000, 500
                            screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
                            pygame.display.update()
                            spikes = pygame.sprite.Group()
                            spikes.add(Spike("spike_big1.png"))
                            spikes.add(Spike("spike_big2.png"))
                            spikes.add(Spike("spike_big4.png"))
                            spikes.add(Spike("spike_small1.png"))
                            spikes.add(Spike("spike_small2.png"))
                            spikes.add(Spike("spike_small3.png"))
                            dino = Dino()
                            poles = pygame.sprite.Group()
                            poles.add(Pole(0, 430))
                            poles.add(Pole(2400, 430))
                            new_game = NewGame()
            if event.type == pygame.MOUSEBUTTONUP:
                moving = False
                tap_mouse = False
            if event.type == pygame.MOUSEMOTION:
                if moving:
                    x += event.pos[0] - x_
                    y += event.pos[1] - y_
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if start:
                        start = False
                        size = width, height = 752, 787
                        screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
                        pygame.display.update()
                    else:
                        running = False
                if event.key == pygame.K_SPACE:
                    if start and not game_over:
                        tap_space = True
                if event.key == pygame.K_RETURN:
                    if start and game_over:
                        time.sleep(0.2)
                        game_over = False
                        jump = False
                        count = 0
                        count_j = 100
                        size = width, height = 1000, 500
                        screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
                        pygame.display.update()
                        spikes = pygame.sprite.Group()
                        spikes.add(Spike("spike_big1.png"))
                        spikes.add(Spike("spike_big2.png"))
                        spikes.add(Spike("spike_big4.png"))
                        spikes.add(Spike("spike_small1.png"))
                        spikes.add(Spike("spike_small2.png"))
                        spikes.add(Spike("spike_small3.png"))
                        dino = Dino()
                        poles = pygame.sprite.Group()
                        poles.add(Pole(0, 430))
                        poles.add(Pole(2400, 430))
                        new_game = NewGame()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    tap_space = False
        window.position = (x, y)
        screen.fill((9, 5, 13))
        pygame.draw.rect(screen, (230, 5, 64), (0, 0, width, height), 5, border_radius=5)
        pygame.draw.rect(screen, (230, 5, 64), (0, 35, width, 5))
        font = pygame.font.SysFont("arial", 27)
        font.set_bold(True)
        text = font.render("Д и н о з а в р и к", False, (230, 5, 64))
        screen.blit(text, (35, 2))
        pygame.draw.circle(screen, (230, 5, 64), (width - 20, 20), 11, 3)
        pygame.draw.polygon(screen, (230, 5, 64),
                            ((width - 27, 15), (width - 25, 13), (width - 13, 25), (width - 15, 27)))
        pygame.draw.polygon(screen, (230, 5, 64),
                            ((width - 13, 15), (width - 15, 13), (width - 27, 25), (width - 25, 27)))
        if start:
            if game_over:
                dino.death()
                font = pygame.font.SysFont("arial", 90)
                font.set_bold(True)
                text = font.render("GAME OVER", False, (230, 5, 64))
                screen.blit(text, (100, 150))
                screen.blit(new_game.image, (new_game.rect.x, new_game.rect.y))
            else:
                count += 1
                count_j -= 1
                if tap_space or tap_mouse:
                    if dino.rect.y == 352:
                        jump = True
                        count_j = 32
                if spikes.sprites()[0].rect.x < -155:
                    for i in spikes.sprites():
                        i.rect.x = width + 10
                        i.rect.y = -1000
                    spike = spikes.sprites()[randint(0, len(spikes.sprites())) - 1]
                    spike.rect.y = 440 - spike.rect.height
                spikes.update()
                poles.update()
                dino.update()
            spikes.draw(screen)
            poles.draw(screen)
            screen.blit(dino.image, (dino.rect.x, dino.rect.y))
            font = pygame.font.SysFont("arial", 45)
            font.set_bold(True)
            text = font.render(f"СЧЁТ: {count // 10}", False, (230, 5, 64))
            screen.blit(text, (20, 50))
        else:
            font = pygame.font.SysFont("arial", 100)
            font.set_bold(True)
            text = font.render("Д и н о з а в р и к", False, (230, 5, 64))
            screen.blit(text, (50, 250))
            pygame.draw.rect(screen, (230, 5, 64), (280, 415, 220, 60), 5, border_radius=30)
            font = pygame.font.SysFont("arial", 45)
            font.set_bold(True)
            text = font.render("СТАРТ", False, (230, 5, 64))
            screen.blit(text, (325, 418))
            pygame.draw.rect(screen, (230, 5, 64), (280, 515, 220, 60), 5, border_radius=30)
            font = pygame.font.SysFont("arial", 45)
            font.set_bold(True)
            text = font.render("РЕЙТИНГ", False, (230, 5, 64))
            screen.blit(text, (300, 518))
        pygame.display.flip()
        pygame.time.Clock().tick(100)
    pygame.quit()
