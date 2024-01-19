import pygame
import random
import os
import sys
import pygame_gui


def game():
    WIDTH = 1366
    HEIGHT = 768
    FPS = 60
    GRAVITY = -0.1

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    screen_rect = (0, 0, WIDTH, HEIGHT)

    pygame.display.set_caption("Aquarium")

    clock = pygame.time.Clock()
    game_over = True
    running = True
    pygame.mixer.music.queue('Gi.mp3')
    font_name = pygame.font.match_font('arial')
    musik = {1: "Satisfaction.mp3", 5: "The_road_without_you.mp3", 2: 'Angie.mp3', 3: "Another_Brick_In_The_Wall.mp3",
             4: 'Gi.mp3'}

    m_num = 0
    manager = pygame_gui.UIManager((1366, 768))


    def load_image(name, colorkey=None):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        image = image.convert_alpha()
        return image


    def draw_text(surf, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, "white")
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)


    background = load_image("fon_all.png")
    #pygame.display.set_icon(load_image("iconca.ico"))


    class Particle(pygame.sprite.Sprite):
        # сгенерируем частицы разного размера
        fire = [load_image("bubblee.png", colorkey=-1)]
        for scale in (5, 10, 20):
            fire.append(pygame.transform.scale(fire[0], (scale, scale)))

        def __init__(self, pos, dx, dy):
            super().__init__(all_sprites)
            self.image = random.choice(self.fire)
            self.rect = self.image.get_rect()

            # у каждой частицы своя скорость — это вектор
            self.velocity = [dx, dy]
            # и свои координаты
            self.rect.x, self.rect.y = pos

            # гравитация будет одинаковой (значение константы)
            self.gravity = GRAVITY

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


    def create_particles(position):
        # количество создаваемых частиц
        particle_count = 20
        # возможные скорости
        numbers = range(-5, 6)
        for _ in range(particle_count):
            Particle(position, random.choice(numbers), random.choice(numbers))


    class Perl(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

            self.image = load_image("perl.png")
            self.image = pygame.transform.scale(self.image, (50, 30))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.center = (random.randint(30, WIDTH - 10), random.randint(10, HEIGHT - 50))

        def update(self):
            if pygame.sprite.collide_mask(self, player):
                perls.remove(self)
                all_sprites.remove(self)
                player.score += 1
                newperl()


    class Heart(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

            self.image = load_image("heart.png")
            self.image = pygame.transform.scale(self.image, (60, 70))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.center = ((50 * player.live - 50 * player.live_1 - 10), 80)

        def update(self):
            if player.live_f:
                for i in range(3 - player.live):
                    hearts.remove(self)
                    all_sprites.remove(self)
                player.live_f = False

            if player.live_f1:
                for i in range(player.live - 1):
                    hearts.remove(self)
                    all_sprites.remove(self)

                for i in range(player.live):
                    player.live_1 = i
                    newheart()
                player.live_f1 = False

            if player.el_shark:
                for i in range(3):
                    hearts.remove(self)
                    all_sprites.remove(self)


    class Green_Perl(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = load_image("green_perl.png")
            self.image = pygame.transform.scale(self.image, (46, 23))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.center = (random.randint(10, WIDTH - 10), random.randint(10, HEIGHT - 50))

        def update(self):
            if pygame.sprite.collide_mask(self, player):
                perls.remove(self)
                all_sprites.remove(self)
                if player.live < 3:
                    player.live += 1
                    player.live_f1 = True


    class Blue_Perl(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

            self.image = load_image("blue_perl.png")
            self.image = pygame.transform.scale(self.image, (46, 23))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.center = (random.randint(10, WIDTH - 10), random.randint(10, HEIGHT - 50))

        def update(self):
            if pygame.sprite.collide_mask(self, player):
                perls.remove(self)
                all_sprites.remove(self)
                pygame.time.set_timer(SMALLSPEED, 3000)
                player.score += 5
                player.speed = 3


    class Gold_Perl(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

            self.image = load_image("golden_perl.png")
            self.image = pygame.transform.scale(self.image, (50, 30))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.center = (random.randint(10, WIDTH - 10), random.randint(10, HEIGHT - 50))

        def update(self):
            if pygame.sprite.collide_mask(self, player):
                perls.remove(self)
                all_sprites.remove(self)
                pygame.time.set_timer(BIGSPEED, 3000)
                player.score += 10
                player.speed = 10


    class Eel(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = load_image("eel.png")
            self.image = pygame.transform.scale(self.image, (300, 100))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.center = (WIDTH + 300, random.randint(200, HEIGHT))

        def update(self):
            self.rect.x -= 1
            if pygame.sprite.collide_mask(self, player) and not player.el:
                pygame.time.set_timer(EL, 2500)
                if player.str == "r":
                    player.image = load_image("el_fish_r.png")
                else:
                    player.image = load_image("el_fish_l.png")
                player.image = pygame.transform.scale(player.image, (200, 100))
                player.score -= 10
                player.el = True
            if self.rect.x < -300:
                fishes.remove(self)
                all_sprites.remove(self)


    class Urchin(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = load_image("urchin.png")
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.center = (random.randint(0, WIDTH), HEIGHT - 30)
            self.speedx = -1
            self.speed_f = 1
            self.el = False

        def update(self):
            self.rect.x += self.speedx

            if pygame.sprite.collide_mask(self, player) and not self.el:
                pygame.time.set_timer(URCHIN, 5000)
                self.speedx = 0
                self.el = True

            if self.rect.x >= WIDTH - 51:
                self.speed_f = 1
                if self.el:
                    self.speedx = -10
                else:
                    self.speedx = -1
            elif self.rect.x <= 3:
                self.speed_f = 0
                if self.el:
                    self.speedx = 10
                else:
                    self.speedx = 1


    class Fisher(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = load_image("fisher.png")
            self.image = pygame.transform.scale(self.image, (650, 450))
            self.rect = self.image.get_rect()
            self.rect.center = (WIDTH + 326, random.randint(400, HEIGHT - 280))
            self.speed = -2
            player.background = 2

        def update(self):
            self.rect.x -= 2
            if self.rect.x < -653:
                fishes.remove(self)
                all_sprites.remove(self)
                if player.background != 0:
                    player.background = 3


    class Shark(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = load_image("shark.png")
            self.image = pygame.transform.scale(self.image, (650, 450))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.center = (WIDTH + 326, random.randint(400, HEIGHT - 280))
            self.speed = -1

        def update(self):
            self.rect.x -= 1
            if self.rect.x < -653:
                fishes.remove(self)
                all_sprites.remove(self)
            if pygame.sprite.collide_mask(self, player) and not player.el_shark:
                player.live -= 3
                player.live_f = True
                player.background = 0
                self.speed = 0
                player.speed = 0

                player.el_shark = True


    class Fugu(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = load_image("fugu_l.png")
            self.image = pygame.transform.scale(self.image, (150, 80))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.center = (WIDTH + 50, random.randint(100, HEIGHT - 280))

        def update(self):
            self.rect.x -= 1
            if self.rect.x < -273:
                fishes.remove(self)
                all_sprites.remove(self)
            if pygame.sprite.collide_mask(self, player) and not player.el_fu:
                pygame.time.set_timer(FUGU_EL, 1000)
                self.image = load_image("fugu_s.png")
                self.image = pygame.transform.scale(self.image, (270, 200))
                player.live -= 1
                player.live_f = True
                player.el_fu = True


    class Fish(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = load_image("fishes.png")
            self.image = pygame.transform.scale(self.image, (200, 100))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.center = (random.randint(0, WIDTH), random.randint(40, HEIGHT))

        def update(self):
            self.rect.x -= 1
            if self.rect.x <= -200:
                self.rect.x = WIDTH
            if pygame.sprite.collide_mask(self, player) and not player.el_f:
                pygame.time.set_timer(FISH_EL, 1000)
                player.score -= 1
                player.el_f = True


    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.score = 0
            self.image = load_image("fish_r.png")
            self.image = pygame.transform.scale(self.image, (200, 100))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.center = (WIDTH / 2, HEIGHT / 2)
            self.el = False
            self.el_f = False
            self.el_fu = False
            self.el_shark = False
            self.str = "r"
            self.speed = 8
            self.live = 3
            self.live_1 = 0
            self.live_f = False
            self.live_f1 = False
            self.background = 1

        def update(self):
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.str = "l"
                if self.el:
                    self.image = load_image("el_fish_l.png")
                else:
                    self.image = load_image("fish_l.png")
                self.image = pygame.transform.scale(self.image, (200, 100))
                self.rect.x -= self.speed
            if keystate[pygame.K_RIGHT]:
                self.str = "r"
                if self.el:
                    self.image = load_image("el_fish_r.png")
                else:
                    self.image = load_image("fish_r.png")
                self.image = pygame.transform.scale(self.image, (200, 100))
                self.rect.x += self.speed
            if keystate[pygame.K_UP]:
                self.rect.y -= self.speed
            if keystate[pygame.K_DOWN]:
                self.rect.y += self.speed
            if self.rect.x > WIDTH:
                self.rect.x = -90
            if self.rect.x < -190:
                self.rect.x = WIDTH
            if self.rect.y > HEIGHT:
                self.rect.y = -90
            if self.rect.y < -90:
                self.rect.y = HEIGHT


    # Функция, создающая аквариумных рыбок
    def newfish():
        fish = Fish()
        all_sprites.add(fish)
        fishes.add(fish)


    # Функция, создающая электрических угрей
    def neweel():
        e = Eel()
        all_sprites.add(e)
        fishes.add(e)


    # Функция, создающая акулу
    def newshark():
        s = Shark()
        all_sprites.add(s)
        fishes.add(s)


    # Функция, создающая удильщика
    def newfisher():
        fi = Fisher()
        all_sprites.add(fi)
        fishes.add(fi)


    # Функция, создающая рыбу фугу
    def newfugu():
        fu = Fugu()
        all_sprites.add(fu)
        fishes.add(fu)


    # Функция, создающая жемчужины
    def newperl():
        p = Perl()
        all_sprites.add(p)
        perls.add(p)


    # Функция, создающая золотые жемчужины
    def newgoldperl():
        p = Gold_Perl()
        all_sprites.add(p)
        perls.add(p)


    # Функция, создающая сердца
    def newheart():
        h = Heart()
        all_sprites.add(h)
        hearts.add(h)


    # Функция, создающая зеленые жемчужины
    def newgreenperl():
        p = Green_Perl()
        all_sprites.add(p)
        perls.add(p)


    # Функция, создающая голубые жемчужины
    def newblueperl():
        p = Blue_Perl()
        all_sprites.add(p)
        perls.add(p)


    def game_over():
        for sprites in all_sprites:
            sprites.kill()




    while running:
        if game_over:

            GOLGPERL = pygame.USEREVENT + 1
            pygame.time.set_timer(GOLGPERL, 30000)

            EL = pygame.USEREVENT + 2
            pygame.time.set_timer(EL, 0)

            EeL_POW = pygame.USEREVENT + 3
            pygame.time.set_timer(EeL_POW, random.randint(20000, 70000))

            BIGSPEED = pygame.USEREVENT + 4
            pygame.time.set_timer(BIGSPEED, 3000)

            SMALLSPEED = pygame.USEREVENT + 5
            pygame.time.set_timer(SMALLSPEED, 3000)

            URCHIN = pygame.USEREVENT + 6
            pygame.time.set_timer(URCHIN, 0)

            FISH_EL = pygame.USEREVENT + 7
            pygame.time.set_timer(FISH_EL, 0)

            Fugu_POW = pygame.USEREVENT + 8
            pygame.time.set_timer(Fugu_POW, random.randint(45000, 200000))

            FUGU_EL = pygame.USEREVENT + 9
            pygame.time.set_timer(FUGU_EL, 0)

            BLUEPERL = pygame.USEREVENT + 12
            pygame.time.set_timer(BLUEPERL, random.randint(15000, 70000))

            GREENPERL = pygame.USEREVENT + 13
            pygame.time.set_timer(GREENPERL, random.randint(75000, 150000))

            SHARK = pygame.USEREVENT + 14
            pygame.time.set_timer(SHARK, 10000)

            FISHER = pygame.USEREVENT + 15
            pygame.time.set_timer(FISHER, random.randint(100000, 150000))

            BLACK = pygame.USEREVENT + 16
            pygame.time.set_timer(BLACK, 7000)

            game_over = False

            all_sprites = pygame.sprite.Group()
            fishes = pygame.sprite.Group()
            perls = pygame.sprite.Group()
            hearts = pygame.sprite.Group()

            player = Player()
            urchin = Urchin()

            all_sprites.add(urchin)
            all_sprites.add(player)

            for i in range(4):
                newfish()
            for i in range(5):
                newperl()
            for i in range(player.live):
                player.live_1 = i
                newheart()
            if player.live <= 0:
                game_over()

            score = 0

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == GOLGPERL:
                newgoldperl()

            if event.type == BLUEPERL:
                newblueperl()

            if event.type == GREENPERL:
                newgreenperl()

            if event.type == SHARK:
                newshark()

            if event.type == FISHER:
                newfisher()

            if event.type == EL:
                pygame.time.set_timer(EL, 0)
                if player.str == "r":
                    player.image = load_image("fish_r.png")
                else:
                    player.image = load_image("fish_l.png")
                player.image = pygame.transform.scale(player.image, (200, 100))
                player.el = False

            if event.type == EeL_POW:
                neweel()

            if event.type == Fugu_POW:
                newfugu()

            if event.type == BIGSPEED:
                pygame.time.set_timer(BIGSPEED, 0)
                player.speed = 8

            if event.type == BLACK:
                pygame.time.set_timer(BLACK, 0)
                player.background = 3

            if event.type == SMALLSPEED:
                pygame.time.set_timer(SMALLSPEED, 0)
                player.speed = 8

            if event.type == URCHIN:
                pygame.time.set_timer(URCHIN, 0)
                if urchin.speed_f == 1:
                    urchin.speedx = -1
                else:
                    urchin.speedx = 1
                urchin.el = False

            if event.type == FISH_EL:
                pygame.time.set_timer(FISH_EL, 0)
                player.el_f = False

            if event.type == FUGU_EL:
                pygame.time.set_timer(FUGU_EL, 0)
                player.el_fu = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    m_num += 1
                    if m_num > 5:
                        m_num = 1
                    pygame.mixer.music.load(musik.get(m_num))
                    pygame.mixer.music.play(-1)
                if event.key == pygame.K_p:
                    pygame.mixer.music.pause()
                if event.key == pygame.K_u:
                    pygame.mixer.music.unpause()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # создаём частицы по щелчку мыши
                create_particles(pygame.mouse.get_pos())

        if player.background == 0:
            background = load_image("blood.png")
        elif player.background == 2:
            background = load_image("black.png")
        elif player.background == 3:
            background = load_image("fon_all.png")
            player.background = 1

        screen.blit(background, (0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        draw_text(screen, str(player.score), 40, 30, 10)
        pygame.display.flip()
    pygame.quit()


game()