import random

import pygame


class MovingSquare:
    def __init__(self):
        self.color = 0
        self.pos = [10, 10]
        self.dx, self.dy = 0, 0

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.dx = 10
            elif event.key == pygame.K_LEFT:
                self.dx = -10
            elif event.key == pygame.K_UP:
                self.dy = -10
            elif event.key == pygame.K_DOWN:
                self.dy = 10
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                self.dx = 0
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                self.dy = 0

    def move(self):
        self.color = (self.color + 1) % 256
        self.pos[0] += self.dx
        self.pos[1] += self.dy

    def draw(self, screen):
        screen.fill((self.color, self.color, self.color), (*self.pos, 50, 50))


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    running = True
    fps = 30
    clock = pygame.time.Clock()
    MY_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(MY_EVENT, 1000)

    ms = MovingSquare()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                ms.process_event(event)
            elif event.type == pygame.KEYUP:
                ms.process_event(event)
            if event.type == MY_EVENT:
                screen.fill((0, 0, 0),
                            (0, 0, width, height))
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                for i in range(100):
                    screen.fill(color,
                                (random.random() * width,
                                 random.random() * height, 5, 5))
        # обновление экрана
        ms.move()
        ms.draw(screen)

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()