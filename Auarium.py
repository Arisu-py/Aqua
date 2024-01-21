import pygame
import pygame_gui
import random
import os
import sys
import sqlite3
import hashlib
from string import digits

STATE, player = 'menu', ''
try:
    def load_image(name, colorkey=None):
        fullname = os.path.join("data", name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        image = image.convert_alpha()
        return image


    def game_over(x):
        WIDTH = 1366
        HEIGHT = 768

        pygame.init()

        screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption("Game_over")
        pygame.display.set_icon(load_image("eel_zn1.ico"))

        font_name = pygame.font.match_font('arial')

        TOTAL = pygame.USEREVENT + 17
        pygame.time.set_timer(TOTAL, 900)

        background = load_image("blood_g.png")
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == TOTAL:
                    running = False
                    total()

            screen.blit(background, (0, 0))
            pygame.display.flip()
        pygame.quit()


    def total():
        global STATE
        pygame.display.set_icon(load_image("eel_zn1.ico"))
        pygame.init()

        pygame.display.set_caption('Total')
        window_surface = pygame.display.set_mode((1366, 768))

        background = pygame.Surface((1366, 768))

        manager = pygame_gui.UIManager((1366, 768))

        window_surface = pygame.display.set_mode((1366, 768))
        f = load_image("fon_total.png")
        background.blit(f, (0, 0))

        name = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((333, 200), (700, 50)),
            text=f'{player.name},',
            manager=manager
        )

        words = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((333, 250), (700, 50)),
            text='it was perfect game!',
            manager=manager
        )

        total_score = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((333, 300), (700, 50)),
            text=f'Total score: {player.score}',
            manager=manager
        )

        max_score = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((333, 350), (700, 50)),
            text=f'Max score: {player.get_max_score()}',
            manager=manager
        )

        menu_b = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((200, 600), (300, 50)),
            text='Menu',
            manager=manager
        )

        end = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((866, 600), (300, 50)),
            text='Exit',
            manager=manager
        )

        clock = pygame.time.Clock()

        run = True

        while run:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect((300, 200), (300, 200)),
                        manager=manager,
                        window_title='Confirm',
                        action_long_desc='Are you sure you want to get out?',
                        action_short_name='OK',
                        blocking=True
                    )
                if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    run = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == menu_b:
                        run = False
                        STATE = 'menu'
                        menu()
                    if event.ui_element == end:
                        confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                            rect=pygame.Rect((333, 160), (300, 200)),
                            manager=manager,
                            window_title='Confirm',
                            action_long_desc='Are you sure you want to get out?',
                            action_short_name='OK',
                            blocking=True
                        )
                manager.process_events(event)
            manager.update(time_delta)
            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
            pygame.display.update()


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
        pygame.display.set_icon(load_image("eel_zn1.ico"))

        clock = pygame.time.Clock()
        game_over = True
        running = True
        pygame.mixer.music.queue('Gi.mp3')
        musik = {1: "Satisfaction.mp3", 5: "The_road_without_you.mp3", 2: 'Angie.mp3',
                 3: "Another_Brick_In_The_Wall.mp3",
                 4: 'Gi.mp3'}

        m_num = 0

        manager = pygame_gui.UIManager((1366, 768))

        font_name = pygame.font.match_font('arial')

        def draw_text(surf, text, size, x, y, color):
            font = pygame.font.Font(font_name, size)
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (x, y)
            surf.blit(text_surface, text_rect)

        background = load_image("fon_all.png")

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
                        all_sprites.remove(self)
                        hearts.remove(self)
                        all_sprites.remove(self)
                        hearts.remove(self)
                        player.live_f = False
                        player.k += 1
                        screen.blit(background, (0, 0))
                        all_sprites.update()
                        all_sprites.draw(screen)
                        pygame.display.flip()

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
                self.k = 0

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

        while running:
            if game_over:

                GOLGPERL = pygame.USEREVENT + 1
                pygame.time.set_timer(GOLGPERL, 30000)

                EL = pygame.USEREVENT + 2
                pygame.time.set_timer(EL, 0)

                EeL_POW = pygame.USEREVENT + 3
                pygame.time.set_timer(EeL_POW, random.randint(20000, 50000))

                BIGSPEED = pygame.USEREVENT + 4
                pygame.time.set_timer(BIGSPEED, 3000)

                SMALLSPEED = pygame.USEREVENT + 5
                pygame.time.set_timer(SMALLSPEED, 3000)

                URCHIN = pygame.USEREVENT + 6
                pygame.time.set_timer(URCHIN, 0)

                FISH_EL = pygame.USEREVENT + 7
                pygame.time.set_timer(FISH_EL, 0)

                Fugu_POW = pygame.USEREVENT + 8
                pygame.time.set_timer(Fugu_POW, random.randint(25000, 45000))

                FUGU_EL = pygame.USEREVENT + 9
                pygame.time.set_timer(FUGU_EL, 0)

                BLUEPERL = pygame.USEREVENT + 12
                pygame.time.set_timer(BLUEPERL, random.randint(25000, 70000))

                GREENPERL = pygame.USEREVENT + 13
                pygame.time.set_timer(GREENPERL, random.randint(35000, 60000))

                SHARK = pygame.USEREVENT + 14
                pygame.time.set_timer(SHARK, random.randint(200000, 250000))

                FISHER = pygame.USEREVENT + 15
                pygame.time.set_timer(FISHER, random.randint(100000, 150000))

                BLACK = pygame.USEREVENT + 16
                pygame.time.set_timer(BLACK, 0)

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
                    running = False

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

                if player.live <= 0:
                    player.speed = 0
                    pygame.time.set_timer(BLACK, 200)

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
            draw_text(screen, str(player.live), 150, 30, 10, "white")
            draw_text(screen, str(player.score), 40, 30, 2, "white")
            pygame.display.flip()
        pygame.quit()
        return player.score


    STATE = 'menu'


    class Player_user:
        def __init__(self, name):
            self.name = name
            self.score = 0

        def different_in_max_score(self, new_score):
            con = sqlite3.connect('players.db')
            result = con.cursor().execute(f"""SELECT score FROM player
                                        WHERE nickname=?
                                        """, (self.name,)).fetchone()
            if result[0] < new_score:
                res = con.cursor().execute(f"""UPDATE player SET score=? WHERE nickname=?
                                        """, (new_score, self.name,))
            con.commit()
            con.close()

        def game_start(self):
            self.score = game()
            self.different_in_max_score(self.score)

        def game_overd(self):
            con = sqlite3.connect('players.db')
            result = con.cursor().execute(f"""SELECT score FROM player WHERE nickname=?
                        """, (self.name,)).fetchone()
            con.close()
            game_over(result[0])

        def get_max_score(self):
            con = sqlite3.connect('players.db')
            result = con.cursor().execute(f"""SELECT score FROM player
                                                WHERE nickname=?
                                                """, (self.name,)).fetchone()
            con.commit()
            con.close()
            return result[0]


    class PasswordError(Exception):
        pass


    class LengthError(PasswordError):
        pass


    class DigitError(PasswordError):
        pass


    class LetterError(PasswordError):
        pass


    class IdentityError(PasswordError):
        pass


    class EmptyNameError(PasswordError):
        pass


    class NicknameError(PasswordError):
        pass


    def menu():
        pygame.init()

        pygame.display.set_caption('Start')
        window_surface = pygame.display.set_mode((1366, 768))
        pygame.display.set_icon(load_image("eel_zn1.ico"))

        background = pygame.Surface((1366, 768))

        manager = pygame_gui.UIManager((1366, 768))

        f = load_image("black.png")
        background.blit(f, (0, 0))

        def main_menu():
            global STATE

            f = load_image("black.png")
            background.blit(f, (0, 0))

            sign_in = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((483, 324), (300, 50)),
                text='Sign in',
                manager=manager
            )

            sign_up = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((483, 404), (300, 50)),
                text='Sign up',
                manager=manager
            )

            end = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((483, 484), (300, 50)),
                text='Exit',
                manager=manager
            )

            d = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((733, 564), (50, 50)),
                text='D',
                manager=manager
            )

            menu_t = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((583, 244), (100, 50)),
                text='Menu',
                manager=manager
            )

            clock = pygame.time.Clock()

            run = True

            while run and STATE == 'menu':
                sign_in.show()
                sign_up.show()
                end.show()
                menu_t.show()
                d.show()
                time_delta = clock.tick(60) / 1000.0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                            rect=pygame.Rect((300, 200), (300, 200)),
                            manager=manager,
                            window_title='Confirm',
                            action_long_desc='Are you sure you want to get out?',
                            action_short_name='OK',
                            blocking=True
                        )
                    if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                        run = False
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == sign_in:
                            sign_in.hide()
                            sign_up.hide()
                            end.hide()
                            menu_t.hide()
                            d.hide()
                            enter()
                        if event.ui_element == sign_up:
                            sign_in.hide()
                            sign_up.hide()
                            end.hide()
                            menu_t.hide()
                            d.hide()
                            registration()
                        if event.ui_element == d:
                            sign_in.hide()
                            sign_up.hide()
                            end.hide()
                            menu_t.hide()
                            d.hide()
                            donate()
                        if event.ui_element == end:
                            confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                                rect=pygame.Rect((333, 160), (300, 200)),
                                manager=manager,
                                window_title='Confirm',
                                action_long_desc='Are you sure you want to get out?',
                                action_short_name='OK',
                                blocking=True
                            )
                    manager.process_events(event)
                manager.update(time_delta)
                window_surface.blit(background, (0, 0))
                manager.draw_ui(window_surface)
                pygame.display.update()

        def registration():
            f = load_image("black.png")
            background.blit(f, (0, 0))

            nickname = pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((343, 240), (400, 50)),
                manager=manager
            )

            password = pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((343, 340), (400, 50)),
                manager=manager
            )
            password.set_text_hidden(is_hidden=True)

            clone_password = pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((343, 440), (400, 50)),
                manager=manager
            )
            clone_password.set_text_hidden(is_hidden=True)

            registrate = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((785, 310), (310, 50)),
                text='Sign up',
                manager=manager
            )

            log = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((783, 370), (314, 50)),
                text='Click if you already have an account',
                manager=manager
            )

            reg_text = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((489, 150), (100, 50)),
                text='Registration',
                manager=manager
            )

            nick_text = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((343, 200), (100, 50)),
                text='Nickname:',
                manager=manager
            )

            pass_text = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((343, 300), (100, 50)),
                text='Password:',
                manager=manager
            )

            clone_pass_text = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((338, 400), (200, 50)),
                text='Repeat the password:',
                manager=manager
            )

            clue = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((338, 490), (500, 50)),
                text='',
                manager=manager
            )
            clue.set_text('')

            def check_password():
                con = sqlite3.connect('players.db')
                result = con.cursor().execute(f"""SELECT password FROM player
                                WHERE nickname=?
                                """, (nickname.text,)).fetchall()
                clue.set_text('')
                try:
                    if nickname.text == "":
                        raise EmptyNameError
                    if result:
                        raise NicknameError
                    line = password.text
                    line2 = clone_password.text
                    if line != line2:
                        raise IdentityError
                    f = False
                    if len(line) < 9:
                        raise LengthError
                    if line.lower() == line or line.upper() == line:
                        raise LetterError
                    for i in line:
                        if i in digits:
                            f = True
                            break
                    if not f:
                        raise DigitError
                except LetterError:
                    clue.set_text("The password must contain characters of both registers")
                except LengthError:
                    clue.set_text("The password must be more than 8 characters long")
                except DigitError:
                    clue.set_text("The password must contain numbers")
                except IdentityError:
                    clue.set_text("Passwords must match")
                except EmptyNameError:
                    clue.set_text("The user name cannot be empty")
                except NicknameError:
                    clue.set_text("This name is already in use, select another one")
                else:
                    clue.set_text("Congratulations, you have successfully registered")
                    return True

            def sign_up():
                con = sqlite3.connect('players.db')
                con.cursor().execute('INSERT INTO player (nickname, password, score) VALUES (?, ?, ?)',
                                     (nickname.text, (hashlib.md5(password.text.encode())).hexdigest(), 0))
                con.commit()
                con.close()

            clock = pygame.time.Clock()
            running = True
            while running:
                nickname.show()
                password.show()
                clone_password.show()
                registrate.show()
                reg_text.show()
                nick_text.show()
                pass_text.show()
                clone_pass_text.show()
                clue.show()
                log.show()
                time_delta = clock.tick(60) / 1000.0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        nickname.hide()
                        password.hide()
                        clone_password.hide()
                        registrate.hide()
                        reg_text.hide()
                        nick_text.hide()
                        pass_text.hide()
                        clone_pass_text.hide()
                        clue.hide()
                        log.hide()
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == registrate:
                            if check_password():
                                sign_up()
                        if event.ui_element == log:
                            running = False
                            nickname.hide()
                            password.hide()
                            clone_password.hide()
                            registrate.hide()
                            reg_text.hide()
                            nick_text.hide()
                            pass_text.hide()
                            clone_pass_text.hide()
                            clue.hide()
                            log.hide()
                            enter()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                            nickname.hide()
                            password.hide()
                            clone_password.hide()
                            registrate.hide()
                            reg_text.hide()
                            nick_text.hide()
                            pass_text.hide()
                            clone_pass_text.hide()
                            clue.hide()
                            log.hide()
                    manager.process_events(event)
                manager.update(time_delta)
                window_surface.blit(f, (0, 0))
                manager.draw_ui(window_surface)
                pygame.display.update()

        def enter():
            global STATE, player
            nick = pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((343, 260), (400, 50)),
                manager=manager
            )

            password = pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((343, 380), (400, 50)),
                manager=manager
            )
            password.set_text_hidden(is_hidden=True)

            enter_check = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((793, 290), (300, 50)),
                text='Sign in',
                manager=manager
            )

            reg = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((783, 350), (330, 50)),
                text="Click if you don't have an account yet",
                manager=manager
            )

            enter_text = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((489, 170), (100, 50)),
                text='Enter',
                manager=manager
            )

            nick_text = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((343, 215), (100, 50)),
                text='Nickname:',
                manager=manager
            )

            pass_text = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((343, 335), (100, 50)),
                text='Password:',
                manager=manager
            )

            clue = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((338, 490), (500, 50)),
                text='',
                manager=manager
            )
            clue.set_text('')

            def sign_in():
                con = sqlite3.connect('players.db')
                result = con.cursor().execute(f"""SELECT password FROM player
                WHERE nickname=?
                """, (nick.text,)).fetchall()
                con.close()
                clue.set_text('')
                if result:
                    if not (hashlib.md5(password.text.encode())).hexdigest() == result[0][0]:
                        clue.set_text("You made a mistake in your username or password")
                        return False
                    else:
                        return True
                else:
                    clue.set_text("You made a mistake in your username or password")
                    return False

            clock = pygame.time.Clock()
            running = True
            while running:
                nick.show()
                password.show()
                enter_check.show()
                enter_text.show()
                nick_text.show()
                pass_text.show()
                clue.show()
                reg.show()
                time_delta = clock.tick(60) / 1000.0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        nick.hide()
                        password.hide()
                        enter_check.hide()
                        enter_text.hide()
                        nick_text.hide()
                        pass_text.hide()
                        clue.hide()
                        reg.hide()
                        running = False
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == enter_check:
                            if sign_in():
                                running = False
                                STATE = 'game'
                                nick.hide()
                                password.hide()
                                enter_check.hide()
                                enter_text.hide()
                                nick_text.hide()
                                pass_text.hide()
                                clue.hide()
                                reg.hide()
                                player = Player_user(nick.text)
                                player.game_start()
                                player.game_overd()
                        if event.ui_element == reg:
                            running = False
                            nick.hide()
                            password.hide()
                            enter_check.hide()
                            enter_text.hide()
                            nick_text.hide()
                            pass_text.hide()
                            clue.hide()
                            reg.hide()
                            registration()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                            nick.hide()
                            password.hide()
                            enter_check.hide()
                            enter_text.hide()
                            nick_text.hide()
                            pass_text.hide()
                            clue.hide()
                            reg.hide()
                    manager.process_events(event)
                manager.update(time_delta)
                window_surface.blit(f, (0, 0))
                manager.draw_ui(window_surface)
                pygame.display.update()

        def donate():
            menu = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((503, 165), (100, 50)),
                text='Donate',
                manager=manager
            )

            card_text = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((345, 215), (100, 50)),
                text='Card number:',
                manager=manager
            )

            card = pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((343, 260), (400, 50)),
                manager=manager
            )
            card.set_text_hidden(is_hidden=True)

            monce_text = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((343, 315), (100, 50)),
                text='Monce/Year:',
                manager=manager
            )

            card_monce = pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((343, 360), (150, 50)),
                manager=manager
            )

            csv_text = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((500, 315), (100, 50)),
                text='CVC/CVV:',
                manager=manager
            )

            card_csv = pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((513, 360), (150, 50)),
                manager=manager
            )
            card_csv.set_text_hidden(is_hidden=True)

            summ_text = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((339, 415), (100, 50)),
                text='How much?:',
                manager=manager
            )

            summ = pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((343, 460), (150, 50)),
                manager=manager
            )

            ok = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((833, 310), (100, 50)),
                text='OK',
                manager=manager
            )

            clue = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((338, 510), (500, 50)),
                text='',
                manager=manager
            )
            clue.set_text('')

            clock = pygame.time.Clock()
            running = True

            def get_card_number():
                card_num = card.text
                card_num = ''.join(card_num.split())
                if card_num.isdigit() and len(card_num) == 16:
                    return card_num
                else:
                    return 404

            def double(x):
                res = x * 2
                if res > 9:
                    res = res - 9
                return res

            def luhn_algorithm():
                n = card.text
                odd = map(lambda x: double(int(x)), n[::2])
                even = map(int, n[1::2])
                return (sum(odd) + sum(even)) % 10 == 0

            def date_and_cs():
                if not card_monce.text or len(card_monce.text) > 5 or len(card_monce.text) < 5 or \
                        not card_monce.text[:1].isdigit() or not card_monce.text[:1].isdigit() or \
                        not card_monce.text[2] == '/':
                    return 101
                month, year = card_monce.text.split('/')
                card_csv.set_text_hidden(True)
                if not (0 < int(month) < 13 and int(year) > 23):
                    return 101
                elif len(card_csv.text) != 3 or not card_csv.text.isdigit():
                    return 102

            def checking():
                number = get_card_number()
                number2 = date_and_cs()
                if number == 404:
                    clue.set_text(
                        "Enter only 16 digits. Spaces are allowed")
                elif not luhn_algorithm():
                    clue.set_text(
                        "The number is invalid. Try again.")
                elif number2 == 101:
                    clue.set_text(
                        "The wrong date was entered. Try again.")
                elif number2 == 102:
                    clue.set_text(
                        "Error in the CVC/CVV code. Try again.")
                elif not summ.text or int(summ.text) < 0:
                    clue.set_text('The payment amount was entered incorrectly.')
                else:
                    clue.set_text('Completed successfully. Thanks)')
                    pygame.mixer.music.load("money.mp3")
                    pygame.mixer.music.play(0)

            while running:
                menu.show()
                card.show()
                card_text.show()
                monce_text.show()
                card_monce.show()
                csv_text.show()
                card_csv.show()
                summ.show()
                summ_text.show()
                ok.show()
                clue.show()
                time_delta = clock.tick(60) / 1000.0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                            rect=pygame.Rect((300, 200), (300, 200)),
                            manager=manager,
                            window_title='Confirm',
                            action_long_desc='Are you sure you want to get out? All data will be lost.',
                            action_short_name='OK',
                            blocking=True
                        )
                    if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                        run = False
                        running = False
                        menu.hide()
                        card.hide()
                        card_text.hide()
                        monce_text.hide()
                        card_monce.hide()
                        csv_text.hide()
                        card_csv.hide()
                        summ.hide()
                        summ_text.hide()
                        ok.hide()
                        clue.hide()
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == ok:
                            checking()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                                rect=pygame.Rect((300, 200), (300, 200)),
                                manager=manager,
                                window_title='Confirm',
                                action_long_desc='Are you sure you want to get out? All data will be lost.',
                                action_short_name='OK',
                                blocking=True
                            )
                    manager.process_events(event)
                manager.update(time_delta)
                window_surface.blit(f, (0, 0))
                manager.draw_ui(window_surface)
                pygame.display.update()

        main_menu()


    menu()
except Exception:
    pass
