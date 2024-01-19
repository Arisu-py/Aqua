import pygame
import pygame_gui
import os
import sys
import sqlite3
import hashlib
from string import digits
#from b import game

STATE = 'menu'


class Player:
    def __init__(self, name):
        self.name = name

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

    #def game_start(self):
        #game()


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


if __name__ == '__main__':
    pygame.init()

    pygame.display.set_caption('Start')
    window_surface = pygame.display.set_mode((700, 400))

    background = pygame.Surface((800, 600))

    background.fill(pygame.Color("#00416a"))
    manager = pygame_gui.UIManager((800, 600))


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


    def main_menu():
        global STATE
        sign_in = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((370, 90), (300, 50)),
            text='Sign in',
            manager=manager
        )

        sign_up = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((370, 170), (300, 50)),
            text='Sign up',
            manager=manager
        )

        end = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((370, 250), (300, 50)),
            text='Exit',
            manager=manager
        )

        d = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((620, 330), (50, 50)),
            text='D',
            manager=manager
        )

        menu = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((470, 20), (100, 50)),
            text='Menu'
        )

        image = load_image("screen-1.jpg")

        clock = pygame.time.Clock()

        run = True

        #if STATE == 'game':
            #game()

        while run and STATE == 'menu':
            sign_in.show()
            sign_up.show()
            end.show()
            menu.show()
            d.show()
            background.blit(image, (10, 80))
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
                        menu.hide()
                        d.hide()
                        enter()
                    if event.ui_element == sign_up:
                        sign_in.hide()
                        sign_up.hide()
                        end.hide()
                        menu.hide()
                        d.hide()
                        registration()
                    if event.ui_element == d:
                        sign_in.hide()
                        sign_up.hide()
                        end.hide()
                        menu.hide()
                        d.hide()
                        donate()
                    if event.ui_element == end:
                        confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                            rect=pygame.Rect((0, 0), (300, 200)),
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
        nickname = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((10, 80), (400, 50)),

        )

        password = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((10, 180), (400, 50)),
        )
        password.set_text_hidden(is_hidden=True)

        clone_password = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((10, 280), (400, 50))
        )
        clone_password.set_text_hidden(is_hidden=True)

        registrate = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((450, 180), (200, 50)),
            text='Sign up',
            manager=manager
        )

        reg_text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 5), (100, 50)),
            text='Registration'
        )

        nick_text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 40), (100, 50)),
            text='Nickname:'
        )

        pass_text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 140), (100, 50)),
            text='Password:'
        )

        clone_pass_text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((5, 240), (200, 50)),
            text='Repeat the password:'
        )

        clue = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((5, 330), (500, 50)),
            text=''
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
                    print(4)
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
                sign_up()

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
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == registrate:
                        if check_password():
                            pass

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        nickname.hide()
                        password.hide()
                        clone_password.hide()
                        registrate.hide()
                        reg_text.hide()
                        nick_text.hide()
                        clue.hide()
                manager.process_events(event)
            background.fill('#00416a')
            manager.update(time_delta)
            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
            pygame.display.update()


    def enter():
        global STATE
        nick = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((10, 100), (400, 50))
        )

        password = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((10, 220), (400, 50))
        )
        password.set_text_hidden(is_hidden=True)

        enter_check = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((450, 160), (200, 50)),
            text='Sign in',
            manager=manager
        )

        enter_text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 10), (100, 50)),
            text='Enter'
        )

        nick_text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 55), (100, 50)),
            text='Nickname:'
        )

        pass_text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 175), (100, 50)),
            text='Password:'
        )

        clue = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((5, 330), (500, 50)),
            text=''
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
                            #game()
                            player = Player(nick.text)
                            player.different_in_max_score(10)
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
                manager.process_events(event)
            background.fill('#00416a')
            manager.update(time_delta)
            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
            pygame.display.update()


    def donate():
        menu = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 5), (100, 50)),
            text='Donate'
        )

        card_text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 55), (100, 50)),
            text='Card number:'
        )

        card = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((10, 100), (400, 50))
        )
        card.set_text_hidden(is_hidden=True)

        monce_text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 155), (100, 50)),
            text='Monce/Year::'
        )

        card_monce = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((10, 200), (150, 50))
        )

        csv_text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((160, 155), (100, 50)),
            text='CVC/CVV:'
        )

        card_csv = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((180, 200), (150, 50))
        )
        card_csv.set_text_hidden(is_hidden=True)

        summ_text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 255), (100, 50)),
            text='How much?:'
        )

        summ = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((10, 300), (150, 50))
        )

        ok = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((500, 150), (100, 50)),
            text='OK',
            manager=manager
        )

        clue = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((5, 350), (500, 50)),
            text=''
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
            if not card_monce.text:
                return 101
            month, year = card_monce.text.split('/')
            if not (0 < int(month) < 13 and int(year) < 25):
                return 101

            elif len(card_csv.text) != 3:
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
                    "Error in the csv code. Try again.")
            elif not summ.text or int(summ.text) < 0:
                clue.set_text('The payment amount was entered incorrectly.')
            else:
                clue.set_text('Completed successfully. Thanks)')

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
                manager.process_events(event)
            background.fill('#00416a')
            manager.update(time_delta)
            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
            pygame.display.update()


    main_menu()
