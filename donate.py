import pygame
import pygame_gui

if __name__ == '__main__':
    pygame.init()

    pygame.display.set_caption('Start')
    window_surface = pygame.display.set_mode((700, 400))

    background = pygame.Surface((800, 600))

    background.fill(pygame.Color("green"))
    manager = pygame_gui.UIManager((800, 600))
    def donate():
        card = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((10, 50), (400, 50))
        )
        clock = pygame.time.Clock()
        running = True
        while running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    print("Number of card:", event.text)
                manager.process_events(event)
            manager.update(time_delta)
            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
            pygame.display.update()

    donate()