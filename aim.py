import pygame
from pygame._sdl2 import Window
import time
from random import randint


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("AIM тренажёр")
    size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode(size, pygame.NOFRAME)
    x = 0
    y = 0
    window = Window.from_display_module()
    running = True
    moving = False
    start = False
    win = False
    count = 0
    points = 0
    r = 20
    x_r = randint(r, width - r)
    y_r = randint(40 + r, height - r)
    x_ = 0
    y_ = 0
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
                    if width / 2.5 < x_ < width / 2.5 + 500 and height / 2 < y_ < height / 2 + 100:
                        if not start or win:
                            time.sleep(0.1)
                            win = False
                            start = True
                            count = 0
                            points = 0
                    if x_r - r <= x_ <= x_r + r and y_r - r <= y_ <= y_r + r:
                        if start and not win:
                            x_r = randint(r, width - r)
                            y_r = randint(40 + r, height - r)
                            points += 1
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
        window.position = (x, y)
        screen.fill((9, 5, 13))
        pygame.draw.rect(screen, (230, 5, 64), (0, 0, width, height), 5, border_radius=5)
        pygame.draw.rect(screen, (230, 5, 64), (0, 35, width, 5))
        font = pygame.font.SysFont("arial", 27)
        font.set_bold(True)
        text = font.render("A I M   т р е н а ж ё р", False, (230, 5, 64))
        screen.blit(text, (35, 2))
        pygame.draw.circle(screen, (230, 5, 64), (width - 20, 20), 11, 3)
        pygame.draw.polygon(screen, (230, 5, 64),
                            ((width - 27, 15), (width - 25, 13), (width - 13, 25), (width - 15, 27)))
        pygame.draw.polygon(screen, (230, 5, 64),
                            ((width - 13, 15), (width - 15, 13), (width - 27, 25), (width - 25, 27)))
        if start:
            if not win:
                count += 1
                pygame.draw.circle(screen, (230, 5, 64), (x_r, y_r), r)
            font = pygame.font.SysFont("arial", 27)
            font.set_bold(True)
            text = font.render(f"В Р Е М Я: {60 - count // 60}", False, (230, 5, 64))
            screen.blit(text, (width / 3, 2))
            font = pygame.font.SysFont("arial", 27)
            font.set_bold(True)
            text = font.render(f"С Ч Ё Т: {points}", False, (230, 5, 64))
            screen.blit(text, (width / 3 * 2, 2))
            if 60 - round(count / 60, 2) <= 0:
                win = True
            if win:
                font = pygame.font.SysFont("arial", round(width / 12.8))
                font.set_bold(True)
                text = font.render(f"Y O U   R E S U L T: {points}", False, (230, 5, 64))
                screen.blit(text, (width / 5, height / 5))
                pygame.draw.rect(screen, (230, 5, 64), (width / 2.5, height / 2, 500, 100), 5, border_radius=30)
                font = pygame.font.SysFont("arial", round(width / 19.2))
                font.set_bold(True)
                text = font.render("РЕСТАРТ", False, (230, 5, 64))
                screen.blit(text, (width / 2.3, height / 2.03))
        else:
            font = pygame.font.SysFont("arial", round(width / 12.8))
            font.set_bold(True)
            text = font.render("A I M   т р е н а ж ё р", False, (230, 5, 64))
            screen.blit(text, (width / 5, height / 5))
            pygame.draw.rect(screen, (230, 5, 64), (width / 2.5, height / 2, 500, 100), 5, border_radius=30)
            font = pygame.font.SysFont("arial", round(width / 19.2))
            font.set_bold(True)
            text = font.render("СТАРТ", False, (230, 5, 64))
            screen.blit(text, (width / 2.2, height / 2.03))
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    pygame.quit()
