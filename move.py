import os
import sys
import random
from copy import deepcopy
from itertools import product

import pygame

pygame.init()
size = width, height = 300, 300
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Cr(pygame.sprite.Sprite):
    image = load_image("creature.png")
    move = 10

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Cr.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.rect.x += 10
            elif event.key == pygame.K_LEFT:
                self.rect.x -= 10
            elif event.key == pygame.K_UP:
                self.rect.y -= 10
            elif event.key == pygame.K_DOWN:
                self.rect.y += 10


class GroupCr(pygame.sprite.Group):
    def process_event(self, event):
        for sprite in self.sprites():
            sprite.process_event(event)


if __name__ == '__main__':
    all_sprites = GroupCr()
    #
    # for _ in range(4):
    Cr(all_sprites)

    running = True
    fps = 30
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                all_sprites.process_event(event)

        # обновление экрана
        screen.fill((255, 255, 255))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(fps)
    pygame.quit()