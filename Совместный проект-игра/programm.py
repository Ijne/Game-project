import pygame
import os
import sys
import random
import sqlite3
import datetime

# Готовим игру к работе
pygame.init()
screen = pygame.display.set_mode((1180, 880))
clock = pygame.time.Clock()
FPS = 60

fon_0 = pygame.mixer.Sound('data/audio/fon_0.mp3')
fon_0.set_volume(0.5)
fon_1 = pygame.mixer.Sound('data/audio/fon_1.mp3')
fon_2 = pygame.mixer.Sound('data/audio/fon_2.mp3')
fon_end = pygame.mixer.Sound('data/audio/fon_end.mp3')
fon_end.set_volume(0.5)
birds_audio = pygame.mixer.Sound('data/audio/birds.wav')
birds_audio.set_volume(0.1)
rain_audio = pygame.mixer.Sound('data/audio/rain.wav')
rain_audio.set_volume(0.3)


def play_music(music):
    music.play()


def stop_music(music):
    music.stop()


def volume_music(music, volume):
    music.set_volume(volume)


# Функция загрузки изображений
def load_image(name, colorkey=None):
    fullname = os.path.join('data/images', name)
    if not os.path.isfile(fullname):
        print(f'Not found {fullname}')
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is None:
        image = image.convert_alpha()
    else:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


# Функции и классы загрузочного экрана
class Start_button(pygame.sprite.Sprite):
    image = load_image('start_1.png')
    image_2 = load_image('start_0.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Start_button.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 500
        self.rect.y = 650
        self.flag = 0

    def update(self, arg, pos):
        if arg and self.rect.collidepoint(pos):
            self.image = Start_button.image_2
        else:
            self.image = Start_button.image


class Continue_button(pygame.sprite.Sprite):
    image = load_image('continue_1.png')
    image_2 = load_image('continue_0.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Continue_button.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 440
        self.rect.y = 550
        self.flag = 0

    def update(self, arg, pos):
        if arg and self.rect.collidepoint(pos):
            self.image = Continue_button.image_2
        else:
            self.image = Continue_button.image


class New_button(pygame.sprite.Sprite):
    image = load_image('new_1.png')
    image_2 = load_image('new_0.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = New_button.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 440
        self.rect.y = 640
        self.flag = 0

    def update(self, arg, pos):
        if arg and self.rect.collidepoint(pos):
            self.image = New_button.image_2
        else:
            self.image = New_button.image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon_0.play()
    start_buttons = pygame.sprite.Group()
    Start_button(start_buttons)

    screen_x = -20
    screen_y = -20
    event_x = -777
    event_y = -777

    while True:
        start_background = load_image('start_screen.png')
        screen.blit(start_background, (screen_x, screen_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for sprite in start_buttons:
                    if sprite.rect.collidepoint(event.pos):
                        pygame.mixer.music.load('data/audio/click_effect.wav')
                        pygame.mixer.music.play()
                        return
            if event.type == pygame.MOUSEMOTION:
                start_buttons.update(True, event.pos)
                if event.pos[0] < event_x and event.pos[1] <= event_y:
                    if screen_x < 0:
                        screen_x += 1
                    if screen_y < 0:
                        screen_y += 1
                elif event.pos[0] <= event_x and event.pos[1] > event_y:
                    if screen_x < 0:
                        screen_x += 1
                    if screen_y > -40:
                        screen_y += -1
                elif event.pos[0] > event_x and event.pos[1] <= event_y:
                    if screen_x > -40:
                        screen_x += -1
                    if screen_y < 0:
                        screen_y += 1
                elif event.pos[0] > event_x and event.pos[1] > event_y:
                    if screen_x > -40:
                        screen_x += -1
                    if screen_y > -40:
                        screen_y += -1
                event_x = event.pos[0]
                event_y = event.pos[1]
        start_buttons.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def registration_screen():
    global directory

    continue_buttons = pygame.sprite.Group()
    Continue_button(continue_buttons)
    new_buttons = pygame.sprite.Group()
    New_button(new_buttons)

    screen_x = -20
    screen_y = -20
    event_x = -777
    event_y = -777

    while True:
        start_background = load_image('start_screen.png')
        screen.blit(start_background, (screen_x, screen_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for sprite in continue_buttons:
                    if sprite.rect.collidepoint(event.pos):
                        pygame.mixer.music.load('data/audio/click_effect.wav')
                        pygame.mixer.music.play()
                        fon_0.stop()
                        return
                for sprite in new_buttons:
                    if sprite.rect.collidepoint(event.pos):
                        pygame.mixer.music.load('data/audio/click_effect.wav')
                        pygame.mixer.music.play()
                        update_level_save()
                        fon_0.stop()
                        return
            if event.type == pygame.MOUSEMOTION:
                continue_buttons.update(True, event.pos)
                new_buttons.update(True, event.pos)
                if event.pos[0] < event_x and event.pos[1] <= event_y:
                    if screen_x < 0:
                        screen_x += 1
                    if screen_y < 0:
                        screen_y += 1
                elif event.pos[0] <= event_x and event.pos[1] > event_y:
                    if screen_x < 0:
                        screen_x += 1
                    if screen_y > -40:
                        screen_y += -1
                elif event.pos[0] > event_x and event.pos[1] <= event_y:
                    if screen_x > -40:
                        screen_x += -1
                    if screen_y < 0:
                        screen_y += 1
                elif event.pos[0] > event_x and event.pos[1] > event_y:
                    if screen_x > -40:
                        screen_x += -1
                    if screen_y > -40:
                        screen_y += -1
                event_x = event.pos[0]
                event_y = event.pos[1]
        continue_buttons.draw(screen)
        new_buttons.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def end_screen():
    screen_x = 0
    screen_y = 0
    speed = 50
    FPS = 60

    while True:
        end_background = pygame.transform.scale(load_image('end_screen.jpg'), (1180, 880))
        screen.blit(end_background, (screen_x, screen_y))
        if screen_x < 0:
            screen_x += speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


# Загрузка уровня
def load_level(filename):
    filename = f'data/levels/save/' + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# Функция генерации уровня (создание списка)
def generate_level(level):
    for x in range(len(level)):
        for y in range(len(level[x])):
            board.field[x][y] = level[x][y]


# Функция выбора нового уровня
def choose_level(level, arg):
    x = level[level.find('(') + 1:level.find(',')].strip()
    y = level[level.find(',') + 1:level.find(')')].strip()
    if arg == pygame.K_w:
        if y == '7':
            return False
        return f'level({x}, {int(y) + 1}).txt'
    elif arg == pygame.K_s:
        if y == '-7':
            return False
        return f'level({x}, {int(y) - 1}).txt'
    elif arg == pygame.K_a:
        if x == '-7':
            return False
        return f'level({int(x) - 1}, {y}).txt'
    elif arg == pygame.K_d:
        if x == '7':
            return False
        return f'level({int(x) + 1}, {y}).txt'


# Функция загрузки нового уровня
def reload_level(new_level):
    global level, hero, location, fon_time

    con = sqlite3.connect('data/database.db')
    cur = con.cursor()

    if new_level:
        generate_level(load_level(new_level))
        level = new_level
        x = level[level.find('(') + 1:level.find(',')].strip()
        y = level[level.find(',') + 1:level.find(')')].strip()

        if int(x) < -4 or int(x) > 4 or int(y) < -4 or int(y) > 4:
            fon_time = 0
            location = 'rainy-dale'
            cur.execute(f"""UPDATE location SET location = 'rainy-dale'""")
            con.commit()
            con.close()
        else:
            fon_time = 0
            location = 'forest'
            cur.execute(f"""UPDATE location SET location = 'forest'""")
            con.commit()
            con.close()

        if int(x) == 7 and int(y) == -7:
            con = sqlite3.connect('data/database.db')
            cur = con.cursor()
            fon_time = 0
            location = 'dark-forest'
            cur.execute(f"""UPDATE location SET location = 'dark-forest'""")
            con.commit()
            con.close()

        # Создание спрайтов
        all_sticks.update(False, None)
        all_stones.update(False, None)
        all_grass.update(False, None)
        all_brown_grass.update(False, None)
        all_brown_stones.update(False, None)
        all_dark_grass.update(False, None)
        all_blue_fire.update(False, None)

        all_carrot.update(False, None)
        all_honey.update(False, None)
        all_mushrooms.update(False, None)
        all_berries.update(False, None)

        d_butterfly_sprite.update(False, None)

        npc_1_sprite.update(False, None)
        npc_2_sprite.update(False, None)
        creator_sprite.update(False, None)
        hero_sprite.update(False)

        # Формирование объектов в списке
        for x in range(len(board.field)):
            for y in range(len(board.field[x])):
                if board.field[x][y] == '0':
                    board.field[x][y] = 0
                elif board.field[x][y] == 'S':
                    element = Sticks((x, y), random.randrange(1, 10, 1))
                    board.field[x][y] = element
                    Sticks_image(element, all_sticks)
                elif board.field[x][y] == 'T':
                    element = Stones((x, y), random.randrange(1, 10, 1))
                    board.field[x][y] = element
                    Stones_image(element, all_stones)
                elif board.field[x][y] == 'G':
                    element = Grass((x, y), random.randrange(1, 10, 1))
                    board.field[x][y] = element
                    Grass_image(element, all_grass)
                elif board.field[x][y] == 't':
                    element = Brown_Stones((x, y), random.randrange(1, 10, 1))
                    board.field[x][y] = element
                    Browns_Stones_image(element, all_brown_stones)
                elif board.field[x][y] == 'g':
                    element = Brown_Grass((x, y), random.randrange(1, 10, 1))
                    board.field[x][y] = element
                    Borwn_Grass_image(element, all_brown_grass)
                elif board.field[x][y] == 'U':
                    element = Dark_grass((x, y), random.randrange(1, 10, 1))
                    board.field[x][y] = element
                    Dark_grass_image(element, all_dark_grass)
                elif board.field[x][y] == 'F':
                    element = Blue_fire((x, y), random.randrange(1, 10, 1))
                    board.field[x][y] = element
                    Blue_fire_image(element, all_blue_fire)

                elif board.field[x][y] == 'C':
                    element = Carrot((x, y))
                    board.field[x][y] = element
                    Carrot_image(element, all_carrot)
                elif board.field[x][y] == 'H':
                    element = Honey((x, y))
                    board.field[x][y] = element
                    Honey_image(element, all_honey)
                elif board.field[x][y] == 'M':
                    element = Mushroom((x, y))
                    board.field[x][y] = element
                    Mushroom_image(element, all_mushrooms)
                elif board.field[x][y] == 'B':
                    element = Berries((x, y))
                    board.field[x][y] = element
                    Berries_image(element, all_berries)

                elif board.field[x][y] == '1':
                    element = NPS_1((x, y))
                    board.field[x][y] = element
                    NPS_1_Image(element, npc_1_sprite)
                elif board.field[x][y] == '2':
                    element = NPS_2((x, y))
                    board.field[x][y] = element
                    NPS_2_Image(element, npc_2_sprite)
                elif board.field[x][y] == '3':
                    element = Creator((x, y))
                    board.field[x][y] = element
                    Creator_Image(element, creator_sprite)

        flag = False
        for x in range(len(board.field)):
            if flag:
                break
            for y in range(len(board.field[x])):
                if board.field[x][y] == 0 and x > 9 and y > 9:
                    hero = Hero((x, y))
                    board.field[x][y] = hero
                    Hero_image(hero, hero_sprite)
                    hero_sprite.update(hero)
                    flag = True
                    break

        camera.update(hero)
        for sprite in all_sticks:
            camera.apply(sprite)
        for sprite in all_stones:
            camera.apply(sprite)
        for sprite in all_grass:
            camera.apply(sprite)
        for sprite in all_brown_stones:
            camera.apply(sprite)
        for sprite in all_brown_grass:
            camera.apply(sprite)
        for sprite in all_dark_grass:
            camera.apply(sprite)
        for sprite in all_blue_fire:
            camera.apply(sprite)

        for sprite in all_carrot:
            camera.apply(sprite)
        for sprite in all_honey:
            camera.apply(sprite)
        for sprite in all_mushrooms:
            camera.apply(sprite)
        for sprite in all_berries:
            camera.apply(sprite)

        for sprite in npc_1_sprite:
            camera.apply(sprite)
        for sprite in npc_2_sprite:
            camera.apply(sprite)
        for sprite in creator_sprite:
            camera.apply(sprite)

        top = (hero.position[0] % 10, hero.position[1] % 10)
        if hero.position[0] < 10:
            top = (0, top[1])
        if hero.position[1] < 10:
            top = (top[0], 0)
        if hero.position[0] > 19:
            top = (10, top[1])
        if hero.position[1] > 19:
            top = (top[0], 10)
        bottom = (top[0] + 19, top[1] + 19)

        view.field = []
        for x in range(top[0], bottom[0] + 1):
            column = []
            for y in range(top[1], bottom[1] + 1):
                column.append(board.field[x][y])
            view.field.append(column)


# Функция записи уровня
def update_level(level):
    output = []
    for x in range(len(board.field)):
        s = ''
        for y in range(len(board.field[x])):
            if board.field[x][y] == 0:
                s += '0'
            elif type(board.field[x][y]) == Sticks:
                s += 'S'
            elif type(board.field[x][y]) == Stones:
                s += 'T'
            elif type(board.field[x][y]) == Grass:
                s += 'G'
            elif type(board.field[x][y]) == Brown_Stones:
                s += 't'
            elif type(board.field[x][y]) == Brown_Grass:
                s += 'g'
            elif type(board.field[x][y]) == Dark_grass:
                s += 'U'
            elif type(board.field[x][y]) == Blue_fire:
                s += 'F'

            elif type(board.field[x][y]) == Carrot:
                s += 'C'
            elif type(board.field[x][y]) == Honey:
                s += 'H'
            elif type(board.field[x][y]) == Mushroom:
                s += 'M'
            elif type(board.field[x][y]) == Berries:
                s += 'B'
            elif type(board.field[x][y]) == Hero:
                s += '0'

            elif type(board.field[x][y]) == NPS_1:
                s += '1'
            elif type(board.field[x][y]) == NPS_2:
                s += '2'
            elif type(board.field[x][y]) == Creator:
                s += '3'
        output.append(s + '\n')

    filename = 'data/levels/save/' + level
    with open(filename, 'w') as mapFile:
        mapFile.writelines(output)


def update_level_save():
    con = sqlite3.connect('data/database.db')
    cur = con.cursor()
    for x in range(-7, 8):
        for y in range(-7, 8):
            file_in = open('data/levels/default/' + f'level({x}, {y}).txt', 'r')
            file_out = open('data/levels/save/' + f'level({x}, {y}).txt', 'w')
            file_out.write(file_in.read())
    cur.execute(f"""UPDATE npc SET step = 1
    WHERE name LIKE 'npc_1'""")
    cur.execute(f"""UPDATE npc SET step = 1
    WHERE name LIKE 'npc_2'""")
    cur.execute(f"""UPDATE npc SET step = 1
    WHERE name LIKE 'creator'""")
    cur.execute(f"""UPDATE level SET level = 'level(0, 0).txt'""")
    cur.execute(f"""UPDATE location SET location = 'forest'""")
    cur.execute(f"""UPDATE hp SET hp = 100""")
    cur.execute(f"""UPDATE hunger SET hunger = 100""")
    cur.execute(f"""DELETE FROM inventory WHERE thing = 'stick' or thing = 'stone' or 
    thing = 'carrot' or thing = 'honey' or thing = 'mushroom' or thing = 'berries'""")
    con.commit()
    con.close()


# Вывод текста во второе меню
def print_text(text_coord, message_text):
    top = 0
    for line in message_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        message_rect = string_rendered.get_rect()
        message_rect.x = text_coord[0]
        message_rect.y = text_coord[1] + top
        top += 15
        screen.blit(string_rendered, message_rect)


# Локация разработчика
class Dark_grass_image(pygame.sprite.Sprite):
    image = load_image('grass-dark.png')
    image_2 = load_image('grass-dark(2).png')

    def __init__(self, grass, *group):
        super().__init__(*group)
        self.image = Dark_grass_image.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = grass.position[0] * board.cell_size + board.left
        self.rect.y = grass.position[1] * board.cell_size + board.top

    def update(self, arg, position):
        global message_text
        if not arg:
            self.kill()
        else:
            if self.rect.x > 800 or self.rect.x < 40 or self.rect.y > 800 or self.rect.y < 40:
                if self.rect.collidepoint(position):
                    self.kill()
            elif arg == 'animation' and self.rect.collidepoint(position):
                if self.image == Dark_grass_image.image:
                    self.image = Dark_grass_image.image_2
                else:
                    self.image = Dark_grass_image.image


class Dark_grass:
    def __init__(self, position, number):
        self.number = number
        self.position = position
        self.power = 0


class Blue_fire_image(pygame.sprite.Sprite):
    image = load_image('fire.png')
    image_2 = load_image('fire(2).png')
    image_3 = load_image('fire(3).png')

    def __init__(self, fire, *group):
        super().__init__(*group)
        self.image = Blue_fire_image.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = fire.position[0] * board.cell_size + board.left
        self.rect.y = fire.position[1] * board.cell_size + board.top

    def update(self, arg, position):
        if not arg:
            self.kill()
        else:
            if self.rect.x > 800 or self.rect.x < 40 or self.rect.y > 800 or self.rect.y < 40:
                if self.rect.collidepoint(position):
                    self.kill()
            elif arg == 'animation' and self.rect.collidepoint(position):
                if self.image == Blue_fire_image.image:
                    self.image = Blue_fire_image.image_2
                elif self.image == Blue_fire_image.image_2:
                    self.image = Blue_fire_image.image_3
                else:
                    self.image = Blue_fire_image.image


class Blue_fire:
    def __init__(self, position, number):
        self.number = number
        self.position = position
        self.power = 0


# Создатель
class Creator_Image(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('creator.png'), (160, 160))

    def __init__(self, npc, *group):
        super().__init__(*group)
        self.image = Creator_Image.image
        self.rect = self.image.get_rect()
        self.rect.x = npc.position[0] * board.cell_size + board.left
        self.rect.y = npc.position[1] * board.cell_size + board.top

    def update(self, arg, position):
        if not arg:
            self.kill()
        else:
            if self.rect.x > 800 or self.rect.x < 40 or self.rect.y > 800 or self.rect.y < 40:
                if self.rect.collidepoint(position):
                    self.kill()


class Creator:
    def __init__(self, position):
        self.position = position
        self.name = 'Создатель'
        self.main_step = nps_2_step
        self.questions_1 = [('-Наконец-то ты меня нашёл', '-Наконец-то ты меня нашёл'),
                            ('-Молодец, что дошёл', '-Ты прошёл длинный путь'),
                            ('-Что ты хочешь узнать?', '-У тебя есть вопросы?'), ('-Уходи',
                                                                                  '-Уходи')]

        self.hero_answers_1 = [('E -Это ты Создатель?', 'F -Приклоняюсь пред тобой'),
                               ('E - Да, это было трудно', 'F - Кланяюююсь'),
                               ('E - Твоё имя', 'F - Сколько тебе лет'), ('E - Повинуюсь', 'F - Прошу прощения')]

        self.answers_1 = [('Пусто', 'Пусто'), ('-Да, герой', '-Все так делают'),
                          ('-Легко не бывает', '-Да прекрати уже'),
                          ('-Никто не должен знать', '-Никто не должен знать')]
        self.step = 0
        self.feel = 0

        if self.main_step == 1:
            self.replics = [self.questions_1, self.hero_answers_1, self.answers_1]

    def start_dialog(self):
        global message_text, creator_step
        con = sqlite3.connect('data/database.db')
        cur = con.cursor()
        process = True
        while process:
            screen.blit(background, (0, 0))
            screen.blit(second_menu_background, (880, 640))
            screen.blit(inventory_menu_background, (880, 0))
            if self.main_step > 1:
                process = False
            elif self.step == 0:
                message_text = ['Создатель:', '', self.replics[0][self.step][self.feel], '',
                                self.replics[1][self.step][0], '', self.replics[1][self.step][1]]
            elif self.step <= len(self.replics[0]) - 1:
                message_text = ['Создатель:', '', self.replics[2][self.step][self.feel], '',
                                self.replics[0][self.step][self.feel], '',
                                self.replics[1][self.step][0], '', self.replics[1][self.step][1]]
            else:
                message_text = []
                if creator_step < 2:
                    creator_step += 1
                    cur.execute(f"""UPDATE npc SET step = {creator_step}
                    WHERE name LIKE 'creator'""")
                    con.commit()
                    con.close()
                process = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    update_level(level)
                    terminate()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    self.step += 1
                    self.feel = 0
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    self.step += 1
                    self.feel = 1
                if event.type == pygame.MOUSEMOTION:
                    arrow.rect.x = event.pos[0]
                    arrow.rect.y = event.pos[1]

            # Отрисовка объектов
            all_dark_grass.draw(screen)
            all_blue_fire.draw(screen)

            hero_sprite.draw(screen)

            creator_sprite.draw(screen)
            print_text(text_coord, message_text)

            d_rain_sprite.update('animation', None)

            if pygame.mouse.get_focused():
                pygame.mouse.set_visible(False)
                arrow_sprite.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)


# Класс камеры
class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        if 10 <= hero.position[0]:
            obj.rect.x += self.dx
        if 10 <= hero.position[1]:
            obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        if top[0] <= 10 and hero.position[0] <= 20:
            self.dx = -((target.position[0] - 11) * 40 + 40 + 40 // 2 - 40 // 2)
        if bottom[1] <= 29 and hero.position[1] <= 20:
            self.dy = -((target.position[1] - 11) * 40 + 40 + 40 // 2 - 40 // 2)


# Декорация-бабочка
class D_butterfly(pygame.sprite.Sprite):
    image = load_image('butterfly.png')

    def __init__(self, position, *group):
        super().__init__(*group)
        self.image = D_butterfly.image
        self.rect = self.image.get_rect()
        self.rect.x = position[0] * board.cell_size + board.left
        self.rect.y = position[1] * board.cell_size + board.top

    def update(self, arg, position):
        global message_text
        if not arg:
            self.kill()
        else:
            if arg == 'animation':
                r = random.randrange(0, 10)
                first = random.randrange(-10, 10)
                second = random.randrange(-10, 10)
                if r == 7:
                    self.image = pygame.transform.flip(self.image, True, True)
                elif r == 8:
                    self.image = pygame.transform.flip(self.image, False, True)
                if first > second:
                    self.rect.x += 1
                else:
                    self.rect.y += 1
            elif self.rect.x > 800 or self.rect.x < 40 or self.rect.y > 800 or self.rect.y < 40:
                if self.rect.collidepoint(position):
                    self.kill()


# Декорация-дождь
class D_rain(pygame.sprite.Sprite):
    image = load_image('rain.png')
    image_2 = load_image('rain(2).png')
    image_3 = load_image('rain(3).png')
    blob = load_image('blob.png')

    def __init__(self, position, *group):
        super().__init__(*group)
        r = random.randrange(0, 3)
        if r == 0:
            self.image = D_rain.image
        elif r == 1:
            self.image = D_rain.image_2
        else:
            self.image = D_rain.image_3
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = position[0] * board.cell_size + board.left
        self.rect.y = position[1] * board.cell_size + board.top

    def update(self, arg, position):
        global message_text
        if not arg:
            self.kill()
        else:
            if self.image == D_rain.blob:
                if not pygame.sprite.spritecollideany(self, hero_sprite):
                    self.kill()
            for sprite in hero_sprite:
                if pygame.sprite.collide_mask(self, sprite):
                    self.image = D_rain.blob
                    self.mask = pygame.mask.from_surface(self.image)
            for sprite in all_berries:
                if pygame.sprite.collide_mask(self, sprite):
                    self.image = D_rain.blob
                    self.mask = pygame.mask.from_surface(self.image)
            for sprite in all_sticks:
                if pygame.sprite.collide_mask(self, sprite):
                    self.image = D_rain.blob
                    self.mask = pygame.mask.from_surface(self.image)
            for sprite in all_mushrooms:
                if pygame.sprite.collide_mask(self, sprite):
                    self.image = D_rain.blob
                    self.mask = pygame.mask.from_surface(self.image)
            for sprite in all_brown_grass:
                if pygame.sprite.collide_mask(self, sprite):
                    self.image = D_rain.blob
                    self.mask = pygame.mask.from_surface(self.image)
            for sprite in all_brown_stones:
                if pygame.sprite.collide_mask(self, sprite):
                    self.image = D_rain.blob
                    self.mask = pygame.mask.from_surface(self.image)
            if arg == 'animation':
                if self.image == D_rain.blob and pygame.sprite.spritecollideany(self, hero_sprite):
                    self.rect.y -= 2
                else:
                    self.rect.y += 10
            elif self.rect.x > 800 or self.rect.x < 40 or self.rect.y > 800 or self.rect.y < 40:
                if self.rect.collidepoint(position):
                    self.kill()


# Классы палок
class Sticks_image(pygame.sprite.Sprite):
    image = load_image('sticks.png')

    def __init__(self, stick, *group):
        super().__init__(*group)
        self.image = Sticks_image.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = stick.position[0] * board.cell_size + board.left
        self.rect.y = stick.position[1] * board.cell_size + board.top

    def update(self, arg, position):
        global message_text
        if not arg:
            self.kill()
        else:
            if self.rect.x > 800 or self.rect.x < 40 or self.rect.y > 800 or self.rect.y < 40:
                if self.rect.collidepoint(position):
                    self.kill()
            if arg and self.rect.collidepoint(position):
                if arg == 'kill':
                    message_text = ['"Полезная штука...', '',
                                    '                                    Ваня"']
                    inventory.add_thing('stick')
                    inventory.draw(len(inventory.get_inventory()) - 1)
                    self.kill()


class Sticks:
    hp = 4

    def __init__(self, position, number):
        self.number = number
        self.position = position
        self.power = 0
        self.hp = 4

    def set_hp(self, hp):
        self.hp = hp

    def get_hp(self):
        return self.hp


# Классы камней
class Stones_image(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('stones.png'), (43, 43))

    def __init__(self, stone, *group):
        super().__init__(*group)
        self.image = Stones_image.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = stone.position[0] * board.cell_size + board.left
        self.rect.y = stone.position[1] * board.cell_size + board.top

    def update(self, arg, position):
        global message_text
        if not arg:
            self.kill()
        else:
            if self.rect.x > 800 or self.rect.x < 40 or self.rect.y > 800 or self.rect.y < 40:
                if self.rect.collidepoint(position):
                    self.kill()
            if arg and self.rect.collidepoint(position):
                if arg == 'kill':
                    message_text = ['"Как мне их тоскать...', '',
                                    '                                    Ваня"']
                    inventory.add_thing('stone')
                    inventory.draw(len(inventory.get_inventory()) - 1)
                    self.kill()


class Stones:
    hp = 8

    def __init__(self, position, number):
        self.number = number
        self.position = position
        self.power = 10

    def set_hp(self, hp):
        self.hp = hp

    def get_hp(self):
        return self.hp


# Классы травы
class Grass_image(pygame.sprite.Sprite):
    image = load_image('grass.png')

    def __init__(self, grass, *group):
        super().__init__(*group)
        self.image = Grass_image.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = grass.position[0] * board.cell_size + board.left
        self.rect.y = grass.position[1] * board.cell_size + board.top

    def update(self, arg, position):
        global message_text
        if not arg:
            self.kill()
        else:
            if self.rect.x > 800 or self.rect.x < 40 or self.rect.y > 800 or self.rect.y < 40:
                if self.rect.collidepoint(position):
                    self.kill()
            if arg and self.rect.collidepoint(position):
                if arg == 'kill':
                    message_text = ['"Травка...', '',
                                    '                                    Ваня"']
                    self.kill()


class Grass:
    hp = 1

    def __init__(self, position, number):
        self.number = number
        self.position = position
        self.power = 0
        self.hp = 1

    def set_hp(self, hp):
        self.hp = hp

    def get_hp(self):
        return self.hp


# Классы коричневых камней
class Browns_Stones_image(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('stones-brown.png'), (43, 43))

    def __init__(self, stone, *group):
        super().__init__(*group)
        self.image = Browns_Stones_image.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = stone.position[0] * board.cell_size + board.left
        self.rect.y = stone.position[1] * board.cell_size + board.top

    def update(self, arg, position):
        global message_text
        if not arg:
            self.kill()
        else:
            if self.rect.x > 800 or self.rect.x < 40 or self.rect.y > 800 or self.rect.y < 40:
                if self.rect.collidepoint(position):
                    self.kill()
            if arg and self.rect.collidepoint(position):
                if arg == 'kill':
                    message_text = ['"На удивление лёгкие...', '',
                                    '                                    Ваня"']
                    inventory.add_thing('stone')
                    inventory.draw(len(inventory.get_inventory()) - 1)
                    self.kill()


class Brown_Stones:
    hp = 6

    def __init__(self, position, number):
        self.number = number
        self.position = position
        self.power = 10
        self.hp = 6

    def set_hp(self, hp):
        self.hp = hp

    def get_hp(self):
        return self.hp


# Классы коричневой травы
class Borwn_Grass_image(pygame.sprite.Sprite):
    image = load_image('grass-brown.png')

    def __init__(self, grass, *group):
        super().__init__(*group)
        self.image = Borwn_Grass_image.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = grass.position[0] * board.cell_size + board.left
        self.rect.y = grass.position[1] * board.cell_size + board.top

    def update(self, arg, position):
        global message_text
        if not arg:
            self.kill()
        else:
            if self.rect.x > 800 or self.rect.x < 40 or self.rect.y > 800 or self.rect.y < 40:
                if self.rect.collidepoint(position):
                    self.kill()
            if arg and self.rect.collidepoint(position):
                if arg == 'kill':
                    message_text = ['"Пахнет приятно...', '',
                                    '                                    Ваня"']
                    self.kill()


class Brown_Grass:
    hp = 1

    def __init__(self, position, number):
        self.number = number
        self.position = position
        self.power = 0
        self.hp = 1

    def set_hp(self, hp):
        self.hp = hp

    def get_hp(self):
        return self.hp


# Классы морковки
class Carrot_image(pygame.sprite.Sprite):
    image = load_image('carrot.png')

    def __init__(self, carrot, *group):
        super().__init__(*group)
        self.image = Carrot_image.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = carrot.position[0] * board.cell_size + board.left
        self.rect.y = carrot.position[1] * board.cell_size + board.top

    def update(self, arg, position):
        global message_text
        global inventory
        if not arg:
            self.kill()
        else:
            if self.rect.x > 800 or self.rect.x < 40 or self.rect.y > 800 or self.rect.y < 40:
                if self.rect.collidepoint(position):
                    self.kill()
            if arg and self.rect.collidepoint(position):
                if arg == 'kill':
                    message_text = ['"Отличная морковь...', '',
                                    '                                    Ваня"']
                    inventory.add_thing('carrot')
                    inventory.draw(len(inventory.get_inventory()) - 1)
                    self.kill()


class Carrot:
    hp = 4

    def __init__(self, position):
        self.food = 10
        self.hp = 4
        self.position = position

    def set_hp(self, hp):
        self.hp = hp

    def get_hp(self):
        return self.hp


# Классы ульев
class Honey_image(pygame.sprite.Sprite):
    image = load_image('honey.png')

    def __init__(self, honey, *group):
        super().__init__(*group)
        self.image = Honey_image.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = honey.position[0] * board.cell_size + board.left
        self.rect.y = honey.position[1] * board.cell_size + board.top

    def update(self, arg, position):
        global message_text
        if not arg:
            self.kill()
        else:
            if self.rect.x > 800 or self.rect.x < 40 or self.rect.y > 800 or self.rect.y < 40:
                if self.rect.collidepoint(position):
                    self.kill()
            if arg and self.rect.collidepoint(position):
                if arg == 'kill':
                    message_text = ['"Блин, обляпался...', '',
                                    '                                    Ваня"']
                    inventory.add_thing('honey')
                    inventory.draw(len(inventory.get_inventory()) - 1)
                    self.kill()


class Honey:
    hp = 4

    def __init__(self, position):
        self.food = 20
        self.hp = 4
        self.position = position

    def set_hp(self, hp):
        self.hp = hp

    def get_hp(self):
        return self.hp


# Классы грибов
class Mushroom_image(pygame.sprite.Sprite):
    image = load_image('mushroom.png')

    def __init__(self, mushroom, *group):
        super().__init__(*group)
        self.image = Mushroom_image.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = mushroom.position[0] * board.cell_size + board.left
        self.rect.y = mushroom.position[1] * board.cell_size + board.top

    def update(self, arg, position):
        global message_text
        if not arg:
            self.kill()
        else:
            if self.rect.x > 800 or self.rect.x < 40 or self.rect.y > 800 or self.rect.y < 40:
                if self.rect.collidepoint(position):
                    self.kill()
            if arg and self.rect.collidepoint(position):
                if arg == 'kill':
                    message_text = ['"Надеюсь, это съедобно...', '',
                                    '                                    Ваня"']
                    inventory.add_thing('mushroom')
                    inventory.draw(len(inventory.get_inventory()) - 1)
                    self.kill()


class Mushroom:
    hp = 2

    def __init__(self, position):
        self.food = 20
        self.hp = 2
        self.position = position

    def set_hp(self, hp):
        self.hp = hp

    def get_hp(self):
        return self.hp


# Классы ягод
class Berries_image(pygame.sprite.Sprite):
    image = load_image('berries.png')

    def __init__(self, berries, *group):
        super().__init__(*group)
        self.image = Berries_image.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = berries.position[0] * board.cell_size + board.left
        self.rect.y = berries.position[1] * board.cell_size + board.top

    def update(self, arg, position):
        global message_text
        if not arg:
            self.kill()
        else:
            if self.rect.x > 800 or self.rect.x < 40 or self.rect.y > 800 or self.rect.y < 40:
                if self.rect.collidepoint(position):
                    self.kill()
            if arg and self.rect.collidepoint(position):
                if arg == 'kill':
                    message_text = ['"Выглядят вскусно...', '',
                                    '                                    Ваня"']
                    inventory.add_thing('berries')
                    inventory.draw(len(inventory.get_inventory()) - 1)
                    self.kill()


class Berries:
    hp = 2

    def __init__(self, position):
        self.food = 30
        self.hp = 2
        self.position = position

    def set_hp(self, hp):
        self.hp = hp

    def get_hp(self):
        return self.hp


# Классы героя
class Hero_image(pygame.sprite.Sprite):
    image_90 = load_image('hero_90.png')
    image_0 = load_image('hero_0.png')
    image_180 = load_image('hero_180.png')

    def __init__(self, hero, *group):
        super().__init__(*group)
        self.image = Hero_image.image_90
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = hero.position[0] * board.cell_size + board.left
        self.rect.y = hero.position[1] * board.cell_size + board.top

    def update(self, hero, *args):
        if not hero:
            self.kill()
        else:
            self.image = Hero_image.image_90
            if 10 <= hero.position[0] <= 20:
                self.rect.x = 10 * board.cell_size + board.left
                camera.update(hero)
            else:
                if hero.position[0] < 10:
                    self.rect.x = (top[0] + hero.position[0]) * board.cell_size + board.left
                else:
                    self.rect.x = (hero.position[0] - top[0]) * board.cell_size + board.left
            if 10 <= hero.position[1] <= 20:
                self.rect.y = 10 * board.cell_size + board.top
                camera.update(hero)
            else:
                if hero.position[1] < 10:
                    self.rect.y = (top[1] + hero.position[1]) * board.cell_size + board.left
                else:
                    self.rect.y = (hero.position[1] - top[1]) * board.cell_size + board.left
            if hero.view == 0:
                self.image = Hero_image.image_0
            elif hero.view == 270:
                self.image = pygame.transform.flip(Hero_image.image_90, True, False)
                hero.view = 270
            elif hero.view == 180:
                self.image = Hero_image.image_180
                hero.view = 180


class Hero:
    def __init__(self, position):
        self.hp = 100
        self.position = position
        self.view = 90
        self.weapon = 'arm'
        self.power = 2
        self.weapon_index = 0
        self.hunger = 100

    def set_weapon(self, weapon, power, index):
        self.weapon = weapon
        self.power = power
        self.weapon_index = index

    def get_weapon(self):
        return [self.weapon, self.power, self.weapon_index]

    def set_hunger(self, hunger):
        self.hunger = hunger

    def get_hunger(self):
        return self.hunger

    def set_hp(self, hp):
        self.hp = hp

    def get_hp(self):
        return self.hp

    def move(self, arg):
        if arg == pygame.K_w:
            if board.field[self.position[0]][self.position[1] - 1] == 0 and \
                    board.on_click((self.position[0], self.position[1] - 1)):
                self.position = (self.position[0], self.position[1] - 1)
                self.view = 0
                board.field[hero.position[0]][hero.position[1] + 1] = 0
                board.field[self.position[0]][self.position[1]] = self
                pygame.mixer.music.load('data/audio/grass.wav')
                pygame.mixer.music.play()
            elif not board.on_click((self.position[0], self.position[1] - 1)):
                if choose_level(level, arg):
                    process = True
                    message_text = ['Нажмите E для перехода', 'или F для отмены']
                    while process:
                        print_text(text_coord, message_text)
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                                process = False
                                board.field[self.position[0]][self.position[1]] = self
                                update_level(level)
                                reload_level(choose_level(level, arg))
                                return False
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                                process = False
                            elif event.type == pygame.QUIT:
                                update_level(level)
                                terminate()

                        # Отрисовка объектов
                        all_sticks.draw(screen)
                        all_stones.draw(screen)
                        all_grass.draw(screen)
                        all_brown_grass.draw(screen)
                        all_brown_stones.draw(screen)
                        inventory_arm.draw(screen)
                        inventory_sticks.draw(screen)
                        inventory_stones.draw(screen)
                        inventory_carrots.draw(screen)
                        inventory_honey.draw(screen)
                        inventory_mushroom.draw(screen)
                        inventory_berries.draw(screen)
                        all_dark_grass.draw(screen)

                        all_carrot.draw(screen)
                        all_honey.draw(screen)
                        all_mushrooms.draw(screen)
                        all_berries.draw(screen)

                        hero_sprite.draw(screen)
                        npc_1_sprite.draw(screen)
                        if pygame.mouse.get_focused():
                            pygame.mouse.set_visible(False)
                            arrow_sprite.draw(screen)
                        pygame.display.flip()
                        clock.tick(FPS)

        elif arg == pygame.K_s:
            if board.on_click((self.position[0], self.position[1] + 1)) and \
                    board.field[self.position[0]][self.position[1] + 1] == 0:
                self.position = (self.position[0], self.position[1] + 1)
                self.view = 180
                board.field[hero.position[0]][hero.position[1] - 1] = 0
                board.field[self.position[0]][self.position[1]] = self
                pygame.mixer.music.load('data/audio/grass.wav')
                pygame.mixer.music.play()
            elif not board.on_click((self.position[0], self.position[1] + 1)):
                if choose_level(level, arg):
                    process = True
                    message_text = ['Нажмите E для перехода', 'или F для отмены']
                    while process:
                        print_text(text_coord, message_text)
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                                process = False
                                board.field[self.position[0]][self.position[1]] = self
                                update_level(level)
                                reload_level(choose_level(level, arg))
                                return False
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                                process = False
                            elif event.type == pygame.QUIT:
                                update_level(level)
                                terminate()

                        # Отрисовка объектов
                        all_sticks.draw(screen)
                        all_stones.draw(screen)
                        all_grass.draw(screen)
                        all_brown_grass.draw(screen)
                        all_brown_stones.draw(screen)
                        inventory_arm.draw(screen)
                        inventory_sticks.draw(screen)
                        inventory_stones.draw(screen)
                        inventory_carrots.draw(screen)
                        inventory_honey.draw(screen)
                        inventory_mushroom.draw(screen)
                        inventory_berries.draw(screen)
                        all_dark_grass.draw(screen)

                        all_carrot.draw(screen)
                        all_honey.draw(screen)
                        all_mushrooms.draw(screen)
                        all_berries.draw(screen)

                        hero_sprite.draw(screen)
                        npc_1_sprite.draw(screen)
                        if pygame.mouse.get_focused():
                            pygame.mouse.set_visible(False)
                            arrow_sprite.draw(screen)
                        pygame.display.flip()
                        clock.tick(FPS)

        elif arg == pygame.K_a:
            if board.field[self.position[0] - 1][self.position[1]] == 0 and \
                    board.on_click((self.position[0] - 1, self.position[1])):
                self.position = (self.position[0] - 1, self.position[1])
                self.view = 270
                board.field[hero.position[0] + 1][hero.position[1]] = 0
                board.field[self.position[0]][self.position[1]] = self
                pygame.mixer.music.load('data/audio/grass.wav')
                pygame.mixer.music.play()
            elif not board.on_click((self.position[0] - 1, self.position[1])):
                if choose_level(level, arg):
                    process = True
                    message_text = ['Нажмите E для перехода', 'или F для отмены']
                    while process:
                        print_text(text_coord, message_text)
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                                process = False
                                board.field[self.position[0]][self.position[1]] = self
                                update_level(level)
                                reload_level(choose_level(level, arg))
                                return False
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                                process = False
                            elif event.type == pygame.QUIT:
                                update_level(level)
                                terminate()

                        # Отрисовка объектов
                        all_sticks.draw(screen)
                        all_stones.draw(screen)
                        all_grass.draw(screen)
                        all_brown_grass.draw(screen)
                        all_brown_stones.draw(screen)
                        inventory_arm.draw(screen)
                        inventory_sticks.draw(screen)
                        inventory_stones.draw(screen)
                        inventory_carrots.draw(screen)
                        inventory_honey.draw(screen)
                        inventory_mushroom.draw(screen)
                        inventory_berries.draw(screen)
                        all_dark_grass.draw(screen)

                        all_carrot.draw(screen)
                        all_honey.draw(screen)
                        all_mushrooms.draw(screen)
                        all_berries.draw(screen)

                        hero_sprite.draw(screen)
                        npc_1_sprite.draw(screen)
                        if pygame.mouse.get_focused():
                            pygame.mouse.set_visible(False)
                            arrow_sprite.draw(screen)
                        pygame.display.flip()
                        clock.tick(FPS)

        elif arg == pygame.K_d:
            if board.on_click((self.position[0] + 1, self.position[1])) and \
                    board.field[self.position[0] + 1][self.position[1]] == 0:
                self.position = (self.position[0] + 1, self.position[1])
                self.view = 90
                board.field[hero.position[0] - 1][hero.position[1]] = 0
                board.field[self.position[0]][self.position[1]] = self
                pygame.mixer.music.load('data/audio/grass.wav')
                pygame.mixer.music.play()
            elif not board.on_click((self.position[0] + 1, self.position[1])):
                if choose_level(level, arg):
                    process = True
                    message_text = ['Нажмите E для перехода', 'или F для отмены']
                    while process:
                        print_text(text_coord, message_text)
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                                process = False
                                board.field[self.position[0]][self.position[1]] = self
                                update_level(level)
                                reload_level(choose_level(level, arg))
                                return False
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                                process = False
                            elif event.type == pygame.QUIT:
                                update_level(level)
                                terminate()

                        # Отрисовка объектов
                        all_sticks.draw(screen)
                        all_stones.draw(screen)
                        all_grass.draw(screen)
                        all_brown_grass.draw(screen)
                        all_brown_stones.draw(screen)
                        inventory_arm.draw(screen)
                        inventory_sticks.draw(screen)
                        inventory_stones.draw(screen)
                        inventory_carrots.draw(screen)
                        inventory_honey.draw(screen)
                        inventory_mushroom.draw(screen)
                        inventory_berries.draw(screen)
                        all_dark_grass.draw(screen)

                        all_carrot.draw(screen)
                        all_honey.draw(screen)
                        all_mushrooms.draw(screen)
                        all_berries.draw(screen)

                        hero_sprite.draw(screen)
                        npc_1_sprite.draw(screen)
                        if pygame.mouse.get_focused():
                            pygame.mouse.set_visible(False)
                            arrow_sprite.draw(screen)
                        pygame.display.flip()
                        clock.tick(FPS)

        return True

    def rotate(self, arg):
        if arg == pygame.K_w:
            self.view = 0
        elif arg == pygame.K_s:
            self.view = 180
        elif arg == pygame.K_a:
            self.view = 270
        elif arg == pygame.K_d:
            self.view = 90
        hero_sprite.update(self)

    def take(self, position, rect_position):
        flag = False
        for i in range(position[0] - 1, position[0] + 2):
            for j in range(position[1] - 1, position[1] + 2):
                if board.width - 1 >= i > -1 and j <= board.height - 1 and i > -1:
                    if type(board.field[i][j]) == Hero:
                        if position[0] == i or position[1] == j:
                            if position[0] == i:
                                if position[1] > j:
                                    if hero.view == 180:
                                        flag = True
                                elif position[1] < j:
                                    if hero.view == 0:
                                        flag = True
                            elif position[1] == j:
                                if position[0] > i:
                                    if hero.view == 90:
                                        flag = True
                                elif position[0] < i:
                                    if hero.view == 270:
                                        flag = True
                        if flag:
                            if type(board.field[position[0]][position[1]]) == Sticks:
                                pygame.mixer.music.load('data/audio/tree.wav')
                                pygame.mixer.music.play()
                            elif type(board.field[position[0]][position[1]]) == Stones or \
                                    type(board.field[position[0]][position[1]]) == Brown_Stones:
                                pygame.mixer.music.load('data/audio/stone.wav')
                                pygame.mixer.music.play()
                                pygame.mixer.music.play()
                            elif type(board.field[position[0]][position[1]]) == Grass or \
                                    type(board.field[position[0]][position[1]]) == Brown_Grass:
                                pygame.mixer.music.load('data/audio/grass_0.wav')
                                pygame.mixer.music.play()
                            elif type(board.field[position[0]][position[1]]) == Carrot or \
                                    type(board.field[position[0]][position[1]]) == Mushroom or \
                                    type(board.field[position[0]][position[1]]) == Berries or \
                                    type(board.field[position[0]][position[1]]) == Honey:
                                pygame.mixer.music.load('data/audio/carrot.wav')
                                pygame.mixer.music.play()
                            board.field[position[0]][position[1]] = 0
                            view.field[position[0] - top[0]][position[1] - top[1]] = 0
                            all_sticks.update('kill', rect_position)
                            all_stones.update('kill', rect_position)
                            all_grass.update('kill', rect_position)
                            all_brown_grass.update('kill', rect_position)
                            all_brown_stones.update('kill', rect_position)
                            all_dark_grass.update('kill', rect_position)

                            all_carrot.update('kill', rect_position)
                            all_honey.update('kill', rect_position)
                            all_mushrooms.update('kill', rect_position)
                            all_berries.update('kill', rect_position)


# НПС-Оборванец
class NPS_1_Image(pygame.sprite.Sprite):
    image = load_image('npc-1.png')

    def __init__(self, npc, *group):
        super().__init__(*group)
        self.image = NPS_1_Image.image
        self.rect = self.image.get_rect()
        self.rect.x = npc.position[0] * board.cell_size + board.left
        self.rect.y = npc.position[1] * board.cell_size + board.top

    def update(self, arg, position):
        if not arg:
            self.kill()
        else:
            if self.rect.x > 800 or self.rect.x < 40 or self.rect.y > 800 or self.rect.y < 40:
                if self.rect.collidepoint(position):
                    self.kill()


class NPS_1:
    def __init__(self, position):
        self.position = position
        self.name = 'Оборванец'
        self.main_step = nps_1_step
        self.questions_1 = [('-Кто ты?', '-Кто ты?'), ('-Не мог бы ты мне помочь?', '-Не мог бы ты мне помочь?'),
                            ('-Ну что согласен?', '-Ну что согласен?'), ('-Найди мою палку и принеси',
                                                                         '-Я потерял палку, найди её')]

        self.hero_answers_1 = [('E - Я не помню', 'F - Назови себя'), ('E - Что мне за это будет?', 'F - Нет не хочу'),
                               ('E - Да', 'F - Так уж и быть'), ('E - Постараюсь', 'F - Ладно')]

        self.answers_1 = [('Пусто', 'Пусто'), ('-Так же как и я', '-Я не знаю своего имени'),
                          ('-Я поделюсь морковью', '-Я могу дать морковь'), ('-Тогда слушай', '-Тогда слушай')]
        self.step = 0
        self.feel = 0

        if self.main_step == 1:
            self.replics = [self.questions_1, self.hero_answers_1, self.answers_1]

    def start_dialog(self):
        global message_text, nps_1_step
        con = sqlite3.connect('data/database.db')
        cur = con.cursor()
        process = True
        while process:
            screen.blit(background, (0, 0))
            screen.blit(second_menu_background, (880, 640))
            screen.blit(inventory_menu_background, (880, 0))
            if self.main_step > 1:
                process = False
            elif self.step == 0:
                message_text = ['Оборванец:', '', self.replics[0][self.step][self.feel], '',
                                self.replics[1][self.step][0], '', self.replics[1][self.step][1]]
            elif self.step <= len(self.replics[0]) - 1:
                message_text = ['Оборванец:', '', self.replics[2][self.step][self.feel], '',
                                self.replics[0][self.step][self.feel], '',
                                self.replics[1][self.step][0], '', self.replics[1][self.step][1]]
            else:
                message_text = []
                if nps_1_step < 2:
                    nps_1_step += 1
                    cur.execute(f"""UPDATE npc SET step = {nps_1_step}
                    WHERE name LIKE 'npc_1'""")
                    con.commit()
                    con.close()
                process = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    update_level(level)
                    terminate()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    self.step += 1
                    self.feel = 0
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    self.step += 1
                    self.feel = 1
                if event.type == pygame.MOUSEMOTION:
                    arrow.rect.x = event.pos[0]
                    arrow.rect.y = event.pos[1]

            # Отрисовка объектов
            all_sticks.draw(screen)
            all_stones.draw(screen)
            all_grass.draw(screen)
            all_carrot.draw(screen)
            all_honey.draw(screen)
            hero_sprite.draw(screen)
            npc_1_sprite.draw(screen)
            inventory_arm.draw(screen)
            inventory_sticks.draw(screen)
            inventory_stones.draw(screen)
            inventory_carrots.draw(screen)
            inventory_honey.draw(screen)
            inventory_mushroom.draw(screen)
            inventory_berries.draw(screen)
            print_text(text_coord, message_text)
            if pygame.mouse.get_focused():
                pygame.mouse.set_visible(False)
                arrow_sprite.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)


# НПС-незнакомка
class NPS_2_Image(pygame.sprite.Sprite):
    image = load_image('npc-2.png')

    def __init__(self, npc, *group):
        super().__init__(*group)
        self.image = NPS_2_Image.image
        self.rect = self.image.get_rect()
        self.rect.x = npc.position[0] * board.cell_size + board.left
        self.rect.y = npc.position[1] * board.cell_size + board.top

    def update(self, arg, position):
        if not arg:
            self.kill()
        else:
            if self.rect.x > 800 or self.rect.x < 40 or self.rect.y > 800 or self.rect.y < 40:
                if self.rect.collidepoint(position):
                    self.kill()


class NPS_2:
    def __init__(self, position):
        self.position = position
        self.name = 'Незнакомка'
        self.main_step = nps_2_step
        self.questions_1 = [('-Прошу помоги', '-Прошу помоги'), ('-Так что, ты поможешь?', '-Поможешь мне?'),
                            ('-Я поделюсь запасами', '-У меня есть ягоды'), ('-Принеси мне мой зонт',
                                                                             '-Прошу, найди мой зонт')]

        self.hero_answers_1 = [('E - Что случилось?', 'F - Кто ты?'), ('E - Как же я могу отказать',
                                                                       'F - Мне нужна награда'),
                               ('E - Сойдёт', 'F - Пойдёт'), ('E - Постараюсь', 'F - Ладно')]

        self.answers_1 = [('Пусто', 'Пусто'), ('-Я потеряла зонт', '-Я не знаю своего имени'),
                          ('-Я так рада', '-Ну раз так'), ('-Тогда слушай', '-Тогда слушай')]
        self.step = 0
        self.feel = 0

        if self.main_step == 1:
            self.replics = [self.questions_1, self.hero_answers_1, self.answers_1]

    def start_dialog(self):
        global message_text, nps_2_step
        con = sqlite3.connect('data/database.db')
        cur = con.cursor()
        process = True
        while process:
            screen.blit(background, (0, 0))
            screen.blit(second_menu_background, (880, 640))
            screen.blit(inventory_menu_background, (880, 0))
            if self.main_step > 1:
                process = False
            elif self.step == 0:
                message_text = ['Незнакомка:', '', self.replics[0][self.step][self.feel], '',
                                self.replics[1][self.step][0], '', self.replics[1][self.step][1]]
            elif self.step <= len(self.replics[0]) - 1:
                message_text = ['Незнакомка:', '', self.replics[2][self.step][self.feel], '',
                                self.replics[0][self.step][self.feel], '',
                                self.replics[1][self.step][0], '', self.replics[1][self.step][1]]
            else:
                message_text = []
                if nps_2_step < 2:
                    nps_2_step += 1
                    cur.execute(f"""UPDATE npc SET step = {nps_2_step}
                    WHERE name LIKE 'npc_2'""")
                    con.commit()
                    con.close()
                process = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    update_level(level)
                    terminate()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    self.step += 1
                    self.feel = 0
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    self.step += 1
                    self.feel = 1
                if event.type == pygame.MOUSEMOTION:
                    arrow.rect.x = event.pos[0]
                    arrow.rect.y = event.pos[1]

            # Отрисовка объектов
            all_sticks.draw(screen)
            all_brown_stones.draw(screen)
            all_brown_grass.draw(screen)

            all_mushrooms.draw(screen)
            all_berries.draw(screen)
            hero_sprite.draw(screen)
            inventory_arm.draw(screen)
            inventory_sticks.draw(screen)
            inventory_stones.draw(screen)
            inventory_carrots.draw(screen)
            inventory_honey.draw(screen)
            inventory_mushroom.draw(screen)
            inventory_berries.draw(screen)

            npc_2_sprite.draw(screen)
            print_text(text_coord, message_text)

            d_rain_sprite.update('animation', None)
            d_rain_sprite.draw(screen)

            if pygame.mouse.get_focused():
                pygame.mouse.set_visible(False)
                arrow_sprite.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)


# Класс поля
class Board:
    def __init__(self, width, height, screen):
        self.screen = screen
        self.width = width
        self.height = height
        self.left = 40
        self.top = 40
        self.cell_size = 40
        self.field = [[0] * height for _ in range(width)]

    def render(self):
        for i in range(0, 20):
            for j in range(0, 20):
                pygame.draw.rect(self.screen, pygame.Color('darkslategray'),
                                 (i * self.cell_size + self.left,
                                  j * self.cell_size + self.top,
                                  self.cell_size, self.cell_size), 1)

    def get_cell(self, position):
        return (position[0] - self.left) // self.cell_size, \
               (position[1] - self.top) // self.cell_size

    def on_click(self, cell):
        if cell[0] > self.width - 1 or cell[0] < 0 or cell[1] > self.height - 1 or cell[1] < 0:
            return False
        return True

    def get_click(self, position):
        cell = self.get_cell(position)
        return self.on_click(cell)


class Sticks_Weapon(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('stick.png'), (35, 34))
    image.set_colorkey((255, 255, 255))

    def __init__(self, i, *group):
        super().__init__(*group)
        self.image = Sticks_Weapon.image
        self.rect = self.image.get_rect()
        self.rect.x = 914 + 39 * ((i - 1) % 6)
        self.rect.y = 37 + 38 * ((i - 1) // 6)

    def update(self, arg):
        if arg == 'kill':
            self.kill()


class Stone_Weapon(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('stone.png'), (35, 34))
    image.set_colorkey((255, 255, 255))

    def __init__(self, i, *group):
        super().__init__(*group)
        self.image = Stone_Weapon.image
        self.rect = self.image.get_rect()
        self.rect.x = 914 + 39 * ((i - 1) % 6)
        self.rect.y = 37 + 38 * ((i - 1) // 6)

    def update(self, arg):
        if arg == 'kill':
            self.kill()


class Carrot_Weapon(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('carrot_food.png'), (35, 34))
    image.set_colorkey((255, 255, 255))

    def __init__(self, i, *group):
        super().__init__(*group)
        self.image = Carrot_Weapon.image
        self.rect = self.image.get_rect()
        self.rect.x = 914 + 39 * ((i - 1) % 6)
        self.rect.y = 37 + 38 * ((i - 1) // 6)

    def update(self, arg):
        if arg == 'kill':
            self.kill()


class Honey_Weapon(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('honey_food.png'), (35, 34))
    image.set_colorkey((255, 255, 255))

    def __init__(self, i, *group):
        super().__init__(*group)
        self.image = Honey_Weapon.image
        self.rect = self.image.get_rect()
        self.rect.x = 914 + 39 * ((i - 1) % 6)
        self.rect.y = 37 + 38 * ((i - 1) // 6)

    def update(self, arg):
        if arg == 'kill':
            self.kill()


class Mushroom_Weapon(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('mushroom_food.png'), (35, 34))
    image.set_colorkey((255, 255, 255))

    def __init__(self, i, *group):
        super().__init__(*group)
        self.image = Mushroom_Weapon.image
        self.rect = self.image.get_rect()
        self.rect.x = 914 + 39 * ((i - 1) % 6)
        self.rect.y = 37 + 38 * ((i - 1) // 6)

    def update(self, arg):
        if arg == 'kill':
            self.kill()


class Berries_Weapon(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('berries_food.png'), (35, 34))
    image.set_colorkey((255, 255, 255))

    def __init__(self, i, *group):
        super().__init__(*group)
        self.image = Berries_Weapon.image
        self.rect = self.image.get_rect()
        self.rect.x = 914 + 39 * ((i - 1) % 6)
        self.rect.y = 37 + 38 * ((i - 1) // 6)

    def update(self, arg):
        if arg == 'kill':
            self.kill()


class Arm_Weapon(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('arm.png'), (35, 34))
    image.set_colorkey((255, 255, 255))

    def __init__(self, i, *group):
        super().__init__(*group)
        self.image = Arm_Weapon.image
        self.rect = self.image.get_rect()
        self.rect.x = 914
        self.rect.y = 37

    def update(self, arg):
        if arg == 'kill':
            self.kill()


# Класс инвентаря
class Inventory:
    def __init__(self):
        self.inventory = []

    def get_inventory(self):
        return self.inventory

    def add_thing(self, thing):
        self.inventory.append(thing)

    def delete_thing(self, index):
        del self.inventory[index]

    def draw(self, index):
        global inventory_arm
        global inventory_sticks
        global inventory_stones
        global inventory_carrots
        global inventory_honey
        global inventory_mushroom
        global inventory_berries
        for i in range(index, len(self.inventory)):
            if i > 89:
                break
            if self.inventory[i] == 'arm':
                arm = Arm_Weapon(i, inventory_arm)
            elif self.inventory[i] == 'stick':
                stick = Sticks_Weapon(i + 1, inventory_sticks)
            elif self.inventory[i] == 'stone':
                stone = Stone_Weapon(i + 1, inventory_stones)
            elif self.inventory[i] == 'carrot':
                carrot = Carrot_Weapon(i + 1, inventory_carrots)
            elif self.inventory[i] == 'honey':
                honey = Honey_Weapon(i + 1, inventory_honey)
            elif self.inventory[i] == 'mushroom':
                mushroom = Mushroom_Weapon(i + 1, inventory_mushroom)
            elif self.inventory[i] == 'berries':
                berries = Berries_Weapon(i + 1, inventory_berries)

    def get_cell(self, pos):
        if pos[0] >= 916 and pos[0] <= 952 and pos[1] >= 38 and pos[1] <= 72:
            return 0
        elif pos[0] >= 956 and pos[0] <= 992 and pos[1] >= 38 and pos[1] <= 72:
            return 1
        elif pos[0] >= 996 and pos[0] <= 1032 and pos[1] >= 38 and pos[1] <= 72:
            return 2
        elif pos[0] >= 1036 and pos[0] <= 1072 and pos[1] >= 38 and pos[1] <= 72:
            return 3
        elif pos[0] >= 1076 and pos[0] <= 1112 and pos[1] >= 38 and pos[1] <= 72:
            return 4
        elif pos[0] >= 1116 and pos[0] <= 1152 and pos[1] >= 38 and pos[1] <= 72:
            return 5
        elif pos[0] >= 916 and pos[0] <= 952 and pos[1] >= 76 and pos[1] <= 110:
            return 6
        elif pos[0] >= 956 and pos[0] <= 992 and pos[1] >= 76 and pos[1] <= 110:
            return 7
        elif pos[0] >= 996 and pos[0] <= 1032 and pos[1] >= 76 and pos[1] <= 110:
            return 8
        elif pos[0] >= 1036 and pos[0] <= 1072 and pos[1] >= 76 and pos[1] <= 110:
            return 9
        elif pos[0] >= 1076 and pos[0] <= 1112 and pos[1] >= 76 and pos[1] <= 110:
            return 10
        elif pos[0] >= 1116 and pos[0] <= 1152 and pos[1] >= 76 and pos[1] <= 110:
            return 11
        elif pos[0] >= 916 and pos[0] <= 952 and pos[1] >= 114 and pos[1] <= 148:
            return 12
        elif pos[0] >= 956 and pos[0] <= 992 and pos[1] >= 114 and pos[1] <= 148:
            return 13
        elif pos[0] >= 996 and pos[0] <= 1032 and pos[1] >= 114 and pos[1] <= 148:
            return 14
        elif pos[0] >= 1036 and pos[0] <= 1072 and pos[1] >= 114 and pos[1] <= 148:
            return 15
        elif pos[0] >= 1076 and pos[0] <= 1112 and pos[1] >= 114 and pos[1] <= 148:
            return 16
        elif pos[0] >= 1116 and pos[0] <= 1152 and pos[1] >= 114 and pos[1] <= 148:
            return 17
        elif pos[0] >= 916 and pos[0] <= 952 and pos[1] >= 152 and pos[1] <= 186:
            return 18
        elif pos[0] >= 956 and pos[0] <= 992 and pos[1] >= 152 and pos[1] <= 186:
            return 19
        elif pos[0] >= 996 and pos[0] <= 1032 and pos[1] >= 152 and pos[1] <= 186:
            return 20
        elif pos[0] >= 1036 and pos[0] <= 1072 and pos[1] >= 152 and pos[1] <= 186:
            return 21
        elif pos[0] >= 1076 and pos[0] <= 1112 and pos[1] >= 152 and pos[1] <= 186:
            return 22
        elif pos[0] >= 1116 and pos[0] <= 1152 and pos[1] >= 152 and pos[1] <= 186:
            return 23
        elif pos[0] >= 916 and pos[0] <= 952 and pos[1] >= 190 and pos[1] <= 224:
            return 24
        elif pos[0] >= 956 and pos[0] <= 992 and pos[1] >= 190 and pos[1] <= 224:
            return 25
        elif pos[0] >= 996 and pos[0] <= 1032 and pos[1] >= 190 and pos[1] <= 224:
            return 26
        elif pos[0] >= 1036 and pos[0] <= 1072 and pos[1] >= 190 and pos[1] <= 224:
            return 27
        elif pos[0] >= 1076 and pos[0] <= 1112 and pos[1] >= 190 and pos[1] <= 224:
            return 28
        elif pos[0] >= 1116 and pos[0] <= 1152 and pos[1] >= 190 and pos[1] <= 224:
            return 29
        elif pos[0] >= 916 and pos[0] <= 952 and pos[1] >= 228 and pos[1] <= 262:
            return 30
        elif pos[0] >= 956 and pos[0] <= 992 and pos[1] >= 228 and pos[1] <= 262:
            return 31
        elif pos[0] >= 996 and pos[0] <= 1032 and pos[1] >= 228 and pos[1] <= 262:
            return 32
        elif pos[0] >= 1036 and pos[0] <= 1072 and pos[1] >= 228 and pos[1] <= 262:
            return 33
        elif pos[0] >= 1076 and pos[0] <= 1112 and pos[1] >= 228 and pos[1] <= 262:
            return 34
        elif pos[0] >= 1116 and pos[0] <= 1152 and pos[1] >= 228 and pos[1] <= 262:
            return 35
        elif pos[0] >= 916 and pos[0] <= 952 and pos[1] >= 266 and pos[1] <= 300:
            return 36
        elif pos[0] >= 956 and pos[0] <= 992 and pos[1] >= 266 and pos[1] <= 300:
            return 37
        elif pos[0] >= 996 and pos[0] <= 1032 and pos[1] >= 266 and pos[1] <= 300:
            return 38
        elif pos[0] >= 1036 and pos[0] <= 1072 and pos[1] >= 266 and pos[1] <= 300:
            return 39
        elif pos[0] >= 1076 and pos[0] <= 1112 and pos[1] >= 266 and pos[1] <= 300:
            return 40
        elif pos[0] >= 1116 and pos[0] <= 1152 and pos[1] >= 266 and pos[1] <= 300:
            return 41
        elif pos[0] >= 916 and pos[0] <= 952 and pos[1] >= 304 and pos[1] <= 338:
            return 42
        elif pos[0] >= 956 and pos[0] <= 992 and pos[1] >= 304 and pos[1] <= 338:
            return 43
        elif pos[0] >= 996 and pos[0] <= 1032 and pos[1] >= 304 and pos[1] <= 338:
            return 44
        elif pos[0] >= 1036 and pos[0] <= 1072 and pos[1] >= 304 and pos[1] <= 338:
            return 45
        elif pos[0] >= 1076 and pos[0] <= 1112 and pos[1] >= 304 and pos[1] <= 338:
            return 46
        elif pos[0] >= 1116 and pos[0] <= 1152 and pos[1] >= 304 and pos[1] <= 338:
            return 47
        elif pos[0] >= 916 and pos[0] <= 952 and pos[1] >= 342 and pos[1] <= 376:
            return 48
        elif pos[0] >= 956 and pos[0] <= 992 and pos[1] >= 342 and pos[1] <= 376:
            return 49
        elif pos[0] >= 996 and pos[0] <= 1032 and pos[1] >= 342 and pos[1] <= 376:
            return 50
        elif pos[0] >= 1036 and pos[0] <= 1072 and pos[1] >= 342 and pos[1] <= 376:
            return 51
        elif pos[0] >= 1076 and pos[0] <= 1112 and pos[1] >= 342 and pos[1] <= 376:
            return 52
        elif pos[0] >= 1116 and pos[0] <= 1152 and pos[1] >= 342 and pos[1] <= 376:
            return 53
        elif pos[0] >= 916 and pos[0] <= 952 and pos[1] >= 380 and pos[1] <= 414:
            return 54
        elif pos[0] >= 956 and pos[0] <= 992 and pos[1] >= 380 and pos[1] <= 414:
            return 55
        elif pos[0] >= 996 and pos[0] <= 1032 and pos[1] >= 380 and pos[1] <= 414:
            return 56
        elif pos[0] >= 1036 and pos[0] <= 1072 and pos[1] >= 380 and pos[1] <= 414:
            return 57
        elif pos[0] >= 1076 and pos[0] <= 1112 and pos[1] >= 380 and pos[1] <= 414:
            return 58
        elif pos[0] >= 1116 and pos[0] <= 1152 and pos[1] >= 380 and pos[1] <= 414:
            return 59
        elif pos[0] >= 916 and pos[0] <= 952 and pos[1] >= 418 and pos[1] <= 452:
            return 60
        elif pos[0] >= 956 and pos[0] <= 992 and pos[1] >= 418 and pos[1] <= 452:
            return 61
        elif pos[0] >= 996 and pos[0] <= 1032 and pos[1] >= 418 and pos[1] <= 452:
            return 62
        elif pos[0] >= 1036 and pos[0] <= 1072 and pos[1] >= 418 and pos[1] <= 452:
            return 63
        elif pos[0] >= 1076 and pos[0] <= 1112 and pos[1] >= 418 and pos[1] <= 452:
            return 64
        elif pos[0] >= 1116 and pos[0] <= 1152 and pos[1] >= 418 and pos[1] <= 452:
            return 65
        elif pos[0] >= 916 and pos[0] <= 952 and pos[1] >= 456 and pos[1] <= 490:
            return 66
        elif pos[0] >= 956 and pos[0] <= 992 and pos[1] >= 456 and pos[1] <= 490:
            return 67
        elif pos[0] >= 996 and pos[0] <= 1032 and pos[1] >= 456 and pos[1] <= 490:
            return 68
        elif pos[0] >= 1036 and pos[0] <= 1072 and pos[1] >= 456 and pos[1] <= 490:
            return 69
        elif pos[0] >= 1076 and pos[0] <= 1112 and pos[1] >= 456 and pos[1] <= 490:
            return 70
        elif pos[0] >= 1116 and pos[0] <= 1152 and pos[1] >= 456 and pos[1] <= 490:
            return 71
        elif pos[0] >= 916 and pos[0] <= 952 and pos[1] >= 494 and pos[1] <= 528:
            return 72
        elif pos[0] >= 956 and pos[0] <= 992 and pos[1] >= 494 and pos[1] <= 528:
            return 73
        elif pos[0] >= 996 and pos[0] <= 1032 and pos[1] >= 494 and pos[1] <= 528:
            return 74
        elif pos[0] >= 1036 and pos[0] <= 1072 and pos[1] >= 494 and pos[1] <= 528:
            return 75
        elif pos[0] >= 1076 and pos[0] <= 1112 and pos[1] >= 494 and pos[1] <= 528:
            return 76
        elif pos[0] >= 1116 and pos[0] <= 1152 and pos[1] >= 494 and pos[1] <= 528:
            return 77
        elif pos[0] >= 916 and pos[0] <= 952 and pos[1] >= 532 and pos[1] <= 566:
            return 78
        elif pos[0] >= 956 and pos[0] <= 992 and pos[1] >= 532 and pos[1] <= 566:
            return 79
        elif pos[0] >= 996 and pos[0] <= 1032 and pos[1] >= 532 and pos[1] <= 566:
            return 80
        elif pos[0] >= 1036 and pos[0] <= 1072 and pos[1] >= 532 and pos[1] <= 566:
            return 81
        elif pos[0] >= 1076 and pos[0] <= 1112 and pos[1] >= 532 and pos[1] <= 566:
            return 82
        elif pos[0] >= 1116 and pos[0] <= 1152 and pos[1] >= 532 and pos[1] <= 566:
            return 83
        elif pos[0] >= 916 and pos[0] <= 952 and pos[1] >= 570 and pos[1] <= 604:
            return 84
        elif pos[0] >= 956 and pos[0] <= 992 and pos[1] >= 570 and pos[1] <= 604:
            return 85
        elif pos[0] >= 996 and pos[0] <= 1032 and pos[1] >= 570 and pos[1] <= 604:
            return 86
        elif pos[0] >= 1036 and pos[0] <= 1072 and pos[1] >= 570 and pos[1] <= 604:
            return 87
        elif pos[0] >= 1076 and pos[0] <= 1112 and pos[1] >= 570 and pos[1] <= 604:
            return 88
        elif pos[0] >= 1116 and pos[0] <= 1152 and pos[1] >= 570 and pos[1] <= 604:
            return 89


# Класс инструментов
class Weapon:
    def __init__(self, power, damage):
        self.power = power
        self.damage = damage


# Класс поля зрения
class View:
    def __init__(self):
        self.width = 20
        self.height = 20
        self.left = 40
        self.top = 40
        self.cell_size = 40
        self.field = [[0] * self.height for _ in range(self.width)]

    def get_board_cell(self, position):
        return (position[0] - self.left) // self.cell_size + top[0], \
               (position[1] - self.top) // self.cell_size + top[1]

    def get_cell(self, position):
        return (position[0] - self.left) // self.cell_size, \
               (position[1] - self.top) // self.cell_size

    def on_click(self, cell):
        if cell[0] > self.width - 1 or cell[0] < 0 or cell[1] > self.height - 1 or cell[1] < 0:
            return False
        return True

    def get_click(self, position):
        cell = self.get_cell(position)
        return self.on_click(cell)


class Building:
    def __init__(self):
        pass

    def build(self):
        pass


# Запуск
if __name__ == '__main__':
    con = sqlite3.connect('data/database.db')
    cur = con.cursor()

    # Заставка
    start_screen()

    # Регистрация
    registration_screen()

    # Генерация уровня
    board = Board(30, 30, screen)
    view = View()
    location = cur.execute("""SELECT location FROM location""").fetchone()[0]

    gen_level = load_level(cur.execute("""SELECT level FROM level""").fetchone()[0])
    generate_level(gen_level)
    level = cur.execute("""SELECT level FROM level""").fetchone()[0]

    camera = Camera()
    top = (0, 0)
    bottom = (19, 19)

    nps_1_step = cur.execute("""SELECT step FROM npc
        WHERE name LIKE 'npc_1'""").fetchone()[0]
    nps_2_step = cur.execute("""SELECT step FROM npc
        WHERE name LIKE 'npc_2'""").fetchone()[0]
    creator_step = cur.execute("""SELECT step FROM npc
        WHERE name LIKE 'creator'""").fetchone()[0]

    second_menu_background = load_image('second-menu.png')
    inventory_menu_background = load_image('inventory-menu.png')

    message_clock = 0
    passive_text = 'Passive'
    list_of_messages = [['"Пустота...', '',
                         '                                    Ваня"'],
                        ['"Грущу в одиночестве...', '',
                         '                                    Ваня"'],
                        ['"Ауу...', '',
                         '                                    Ваня"']
                        ]

    decoration_clock = 0
    music_time = 0
    fon_time = 0
    volume = 0
    mus = fon_1

    # Создание курсора
    arrow_sprite = pygame.sprite.Group()
    arrow = pygame.sprite.Sprite()
    arrow.image = load_image('arrow-hand.png')
    arrow.rect = arrow.image.get_rect()
    arrow_sprite.add(arrow)

    # Создание спрайтов
    all_sticks = pygame.sprite.Group()
    all_stones = pygame.sprite.Group()
    all_grass = pygame.sprite.Group()
    all_brown_grass = pygame.sprite.Group()
    all_brown_stones = pygame.sprite.Group()
    all_dark_grass = pygame.sprite.Group()
    all_blue_fire = pygame.sprite.Group()

    all_carrot = pygame.sprite.Group()
    all_honey = pygame.sprite.Group()
    all_mushrooms = pygame.sprite.Group()
    all_berries = pygame.sprite.Group()
    all_stick_walls = pygame.sprite.Group()
    all_stone_walls = pygame.sprite.Group()

    hero_sprite = pygame.sprite.Group()
    npc_1_sprite = pygame.sprite.Group()
    npc_2_sprite = pygame.sprite.Group()
    inventory_arm = pygame.sprite.Group()
    inventory_sticks = pygame.sprite.Group()
    inventory_stones = pygame.sprite.Group()
    inventory_carrots = pygame.sprite.Group()
    inventory_honey = pygame.sprite.Group()
    inventory_mushroom = pygame.sprite.Group()
    inventory_berries = pygame.sprite.Group()
    creator_sprite = pygame.sprite.Group()

    # Спрайты декораций
    d_butterfly_sprite = pygame.sprite.Group()
    d_rain_sprite = pygame.sprite.Group()

    # Текст
    message_text = []

    font = pygame.font.Font(None, 25)
    text_coord = (910, 670)

    # Стартовые инструменты
    inventory = Inventory()
    arr = cur.execute("""SELECT * FROM inventory""").fetchall()
    for i in range(len(arr)):
        inventory.add_thing(arr[i][0])
    inventory.draw(0)

    # Формирование объектов в списке и первоначальная отрисовка
    for x in range(len(board.field)):
        for y in range(len(board.field[x])):
            if board.field[x][y] == '0':
                board.field[x][y] = 0
            elif board.field[x][y] == 'S':
                element = Sticks((x, y), random.randrange(1, 10, 1))
                board.field[x][y] = element
                Sticks_image(element, all_sticks)
            elif board.field[x][y] == 'T':
                element = Stones((x, y), random.randrange(1, 10, 1))
                board.field[x][y] = element
                Stones_image(element, all_stones)
            elif board.field[x][y] == 'G':
                element = Grass((x, y), random.randrange(1, 10, 1))
                board.field[x][y] = element
                Grass_image(element, all_grass)
            elif board.field[x][y] == 't':
                element = Brown_Stones((x, y), random.randrange(1, 10, 1))
                board.field[x][y] = element
                Browns_Stones_image(element, all_brown_stones)
            elif board.field[x][y] == 'g':
                element = Brown_Grass((x, y), random.randrange(1, 10, 1))
                board.field[x][y] = element
                Borwn_Grass_image(element, all_brown_grass)
            elif board.field[x][y] == 'U':
                element = Dark_grass((x, y), random.randrange(1, 10, 1))
                board.field[x][y] = element
                Dark_grass_image(element, all_dark_grass)
            elif board.field[x][y] == 'F':
                element = Blue_fire((x, y), random.randrange(1, 10, 1))
                board.field[x][y] = element
                Blue_fire_image(element, all_blue_fire)

            elif board.field[x][y] == 'C':
                element = Carrot((x, y))
                board.field[x][y] = element
                Carrot_image(element, all_carrot)
            elif board.field[x][y] == 'H':
                element = Honey((x, y))
                board.field[x][y] = element
                Honey_image(element, all_honey)
            elif board.field[x][y] == 'M':
                element = Mushroom((x, y))
                board.field[x][y] = element
                Mushroom_image(element, all_mushrooms)
            elif board.field[x][y] == 'B':
                element = Berries((x, y))
                board.field[x][y] = element
                Berries_image(element, all_berries)

            elif board.field[x][y] == '1':
                element = NPS_1((x, y))
                board.field[x][y] = element
                NPS_1_Image(element, npc_1_sprite)
            elif board.field[x][y] == '2':
                element = NPS_2((x, y))
                board.field[x][y] = element
                NPS_2_Image(element, npc_2_sprite)
            elif board.field[x][y] == '3':
                element = Creator((x, y))
                board.field[x][y] = element
                Creator_Image(element, creator_sprite)

    flag = False
    for x in range(len(board.field)):
        if flag:
            break
        for y in range(len(board.field[x])):
            if board.field[x][y] == 0 and x > 10 and y > 10:
                hero = Hero((x, y))
                board.field[x][y] = hero
                Hero_image(hero, hero_sprite)
                flag = True
                break

    camera.update(hero)
    for sprite in all_sticks:
        camera.apply(sprite)
    for sprite in all_stones:
        camera.apply(sprite)
    for sprite in all_grass:
        camera.apply(sprite)
    for sprite in all_brown_stones:
        camera.apply(sprite)
    for sprite in all_brown_grass:
        camera.apply(sprite)
    for sprite in all_dark_grass:
        camera.apply(sprite)
    for sprite in all_blue_fire:
        camera.apply(sprite)

    for sprite in all_carrot:
        camera.apply(sprite)
    for sprite in all_honey:
        camera.apply(sprite)
    for sprite in all_mushrooms:
        camera.apply(sprite)
    for sprite in all_berries:
        camera.apply(sprite)

    for sprite in npc_1_sprite:
        camera.apply(sprite)
    for sprite in npc_2_sprite:
        camera.apply(sprite)
    for sprite in creator_sprite:
        camera.apply(sprite)

    top = (hero.position[0] % 10, hero.position[1] % 10)
    if hero.position[0] < 10:
        top = (0, top[1])
    if hero.position[1] < 10:
        top = (top[0], 0)
    if hero.position[0] > 19:
        top = (10, top[1])
    if hero.position[1] > 19:
        top = (top[0], 10)
    bottom = (top[0] + 19, top[1] + 19)

    view.field = []
    for x in range(top[0], bottom[0] + 1):
        column = []
        for y in range(top[1], bottom[1] + 1):
            column.append(board.field[x][y])
        view.field.append(column)

    start_time = datetime.datetime.now().time()

    font_object = pygame.font.Font(None, 25)
    font_object2 = pygame.font.Font(None, 25)

    text_hp = font_object.render(f'Здоровье: {hero.get_hp()}', True, ((162, 32, 32)))
    text_hp_rect = text_hp.get_rect()
    text_hp_rect.x = 20
    text_hp_rect.y = 2

    text_hunger = font_object2.render(f'Голод: {hero.get_hunger()}', True, pygame.Color('orange'))
    text_hunger_rect = text_hunger.get_rect()
    text_hunger_rect.x = 200
    text_hunger_rect.y = 2

    hp_db = cur.execute(f"""SELECT hp FROM hp""").fetchone()
    hero.set_hp(hp_db[0])
    hunger_db = cur.execute(f"""SELECT hunger FROM hunger""").fetchone()
    hero.set_hunger(hunger_db[0])

    if hero.get_hp() == 0:
        end_screen()

    sticks_hp = 4
    stones_hp = 6
    grass_hp = 1
    carrots_hp = 4
    honey_hp = 4
    mushroom_hp = 2
    berries_hp = 2

    # Непосредственно запуск
    running = True
    while running:
        if hero.get_hp() == 0:
            stop_music(rain_audio)
            stop_music(birds_audio)
            play_music(fon_end)
            end_screen()
            running = False
        now_time = datetime.datetime.now().time()
        if start_time.hour == now_time.hour:
            if start_time.second + 30 == now_time.second or\
                    start_time.second - 30 == now_time.second:
                if hero.get_hunger() > 0:
                    hero.set_hunger(hero.get_hunger() - 10)
                    if start_time.second + 30 < 60:
                        start_time = start_time.replace(start_time.hour, start_time.minute,
                                                        start_time.second + 30)
                    else:
                        if start_time.minute + 1 < 60:
                            start_time = start_time.replace(start_time.hour, start_time.minute + 1,
                                                            start_time.second - 30)
                        else:
                            if start_time.hour + 1 < 24:
                                start_time = start_time.replace(start_time.hour + 1, 0,
                                                                start_time.second - 30)
                            else:
                                start_time = start_time.replace(0, 0, start_time.second - 30)
        else:
            if start_time.hour + 1 < 24:
                start_time = start_time.replace(start_time.hour + 1, 0, 0)
            else:
                start_time.replace(0, start_time.minute, start_time.second)

        text_hp = font_object.render(f'Здоровье: {hero.get_hp()}', True, (162, 32, 32))
        text_hp_rect = text_hp.get_rect()
        text_hp_rect.x = 20
        text_hp_rect.y = 2

        text_hunger = font_object2.render(f'Голод: {hero.get_hunger()}', True, pygame.Color('orange'))
        text_hunger_rect = text_hunger.get_rect()
        text_hunger_rect.x = 200
        text_hunger_rect.y = 2

        if hero.get_hunger() == 0:
            if start_time.second + 7 == now_time.second:
                if hero.get_hp() > 0:
                    hero.set_hp(hero.get_hp() - 10)
                    if start_time.second + 7 < 60:
                        start_time = start_time.replace(start_time.hour, start_time.minute,
                                                        start_time.second + 7)
                    else:
                        if start_time.minute + 1 < 60:
                            start_time = start_time.replace(start_time.hour, start_time.minute + 1,
                                                            start_time.second - 53)
                        else:
                            if start_time.hour + 1 < 24:
                                start_time = start_time.replace(start_time.hour + 1, 0,
                                                                start_time.second - 53)
                            else:
                                start_time = start_time.replace(0, 0, start_time.second - 53)

        if location == 'forest':
            background = pygame.transform.scale(load_image('background-field.png'), (880, 880))
        elif location == 'rainy-dale':
            background = pygame.transform.scale(load_image('background-brown.png'), (880, 880))
        else:
            background = pygame.transform.scale(load_image('background-dark.png'), (880, 880))
        screen.blit(background, (0, 0))
        screen.blit(second_menu_background, (880, 640))
        screen.blit(inventory_menu_background, (880, 0))
        hp = hero.get_hp()
        hunger = hero.get_hunger()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_a or \
                        event.key == pygame.K_d or event.key == pygame.K_s:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LSHIFT]:
                        hero.rotate(event.key)
                    else:
                        if hero.move(event.key):
                            # Изменнение видимых объектов
                            top = (hero.position[0] % 10, hero.position[1] % 10)
                            if hero.position[0] < 10:
                                top = (0, top[1])
                            if hero.position[1] < 10:
                                top = (top[0], 0)
                            if hero.position[0] > 19:
                                top = (10, top[1])
                            if hero.position[1] > 19:
                                top = (top[0], 10)
                            bottom = (top[0] + 19, top[1] + 19)

                            view.field = []
                            for x in range(top[0], bottom[0] + 1):
                                column = []
                                for y in range(top[1], bottom[1] + 1):
                                    column.append(board.field[x][y])
                                view.field.append(column)

                            hero_sprite.update(hero)

                            all_sticks.update(False, None)
                            all_stones.update(False, None)
                            all_grass.update(False, None)
                            all_brown_stones.update(False, None)
                            all_brown_grass.update(False, None)
                            all_dark_grass.update(False, None)
                            all_blue_fire.update(False, None)

                            all_carrot.update(False, None)
                            all_honey.update(False, None)
                            all_mushrooms.update(False, None)
                            all_berries.update(False, None)

                            npc_1_sprite.update(False, None)
                            npc_2_sprite.update(False, None)
                            creator_sprite.update(False, None)

                            for x in range(len(board.field)):
                                for y in range(len(board.field[x])):
                                    if type(board.field[x][y]) == Sticks:
                                        element = Sticks((x, y), random.randrange(1, 10, 1))
                                        board.field[x][y] = element
                                        Sticks_image(element, all_sticks)
                                    elif type(board.field[x][y]) == Stones:
                                        element = Stones((x, y), random.randrange(1, 10, 1))
                                        board.field[x][y] = element
                                        Stones_image(element, all_stones)
                                    elif type(board.field[x][y]) == Grass:
                                        element = Grass((x, y), random.randrange(1, 10, 1))
                                        board.field[x][y] = element
                                        Grass_image(element, all_grass)
                                    elif type(board.field[x][y]) == Brown_Stones:
                                        element = Brown_Stones((x, y), random.randrange(1, 10, 1))
                                        board.field[x][y] = element
                                        Browns_Stones_image(element, all_brown_stones)
                                    elif type(board.field[x][y]) == Brown_Grass:
                                        element = Brown_Grass((x, y), random.randrange(1, 10, 1))
                                        board.field[x][y] = element
                                        Borwn_Grass_image(element, all_brown_grass)
                                    elif type(board.field[x][y]) == Dark_grass:
                                        element = Dark_grass((x, y), random.randrange(1, 10, 1))
                                        board.field[x][y] = element
                                        Dark_grass_image(element, all_dark_grass)
                                    elif type(board.field[x][y]) == Blue_fire:
                                        element = Blue_fire((x, y), random.randrange(1, 10, 1))
                                        board.field[x][y] = element
                                        Blue_fire_image(element, all_blue_fire)

                                    elif type(board.field[x][y]) == Carrot:
                                        element = Carrot((x, y))
                                        board.field[x][y] = element
                                        Carrot_image(element, all_carrot)
                                    elif type(board.field[x][y]) == Honey:
                                        element = Honey((x, y))
                                        board.field[x][y] = element
                                        Honey_image(element, all_honey)
                                    elif type(board.field[x][y]) == Mushroom:
                                        element = Mushroom((x, y))
                                        board.field[x][y] = element
                                        Mushroom_image(element, all_mushrooms)
                                    elif type(board.field[x][y]) == Berries:
                                        element = Berries((x, y))
                                        board.field[x][y] = element
                                        Berries_image(element, all_berries)

                                    elif type(board.field[x][y]) == NPS_1:
                                        element = NPS_1((x, y))
                                        board.field[x][y] = element
                                        NPS_1_Image(element, npc_1_sprite)
                                    elif type(board.field[x][y]) == NPS_2:
                                        element = NPS_2((x, y))
                                        board.field[x][y] = element
                                        NPS_2_Image(element, npc_2_sprite)
                                    elif type(board.field[x][y]) == Creator:
                                        element = Creator((x, y))
                                        board.field[x][y] = element
                                        Creator_Image(element, creator_sprite)

                            # Смещение объектов
                            camera.update(hero)
                            for sprite in all_sticks:
                                camera.apply(sprite)
                            for sprite in all_stones:
                                camera.apply(sprite)
                            for sprite in all_grass:
                                camera.apply(sprite)
                            for sprite in all_brown_stones:
                                camera.apply(sprite)
                            for sprite in all_brown_grass:
                                camera.apply(sprite)
                            for sprite in all_dark_grass:
                                camera.apply(sprite)
                            for sprite in all_blue_fire:
                                camera.apply(sprite)

                            for sprite in all_carrot:
                                camera.apply(sprite)
                            for sprite in all_honey:
                                camera.apply(sprite)
                            for sprite in all_mushrooms:
                                camera.apply(sprite)
                            for sprite in all_berries:
                                camera.apply(sprite)

                            for sprite in npc_1_sprite:
                                camera.apply(sprite)
                            for sprite in npc_2_sprite:
                                camera.apply(sprite)
                        hero.set_hp(hp)
                        hero.set_hunger(hunger)
                        for sprite in creator_sprite:
                            camera.apply(sprite)

            if event.type == pygame.MOUSEMOTION:
                arrow.rect.x = event.pos[0]
                arrow.rect.y = event.pos[1]
                if view.get_click(event.pos):
                    position = view.get_cell(event.pos)
                    if type(view.field[position[0]][position[1]]) == Sticks:
                        message_text = ['Палки:', '', '"Хотя бы что-то...', '',
                                        '                                    Вы"']
                    elif type(view.field[position[0]][position[1]]) == Stones:
                        message_text = ['Обычный камень:', '', '"Пфф, ничего не обычного...', '',
                                        '                                    Вы"']
                    elif type(view.field[position[0]][position[1]]) == Grass:
                        message_text = ['Зелёная трава:', '', '"В хозяйстве пригодиться...', '',
                                        '                                    Вы"']
                    elif type(view.field[position[0]][position[1]]) == Brown_Grass:
                        message_text = ['Жёлтая трава:', '', '"От неё идёт запах...', '',
                                        '                                    Вы"']
                    elif type(view.field[position[0]][position[1]]) == Dark_grass:
                        message_text = ['Синяя трава:', '', '"Веет холодом...', '',
                                        '                                    Вы"']
                    elif type(view.field[position[0]][position[1]]) == Blue_fire:
                        message_text = ['Мёртвый огонь:', '', '"Это, что газ?...', '',
                                        '                                    Вы"']
                    elif type(view.field[position[0]][position[1]]) == Brown_Stones:
                        message_text = ['Малый камень:', '', '"Камень, как и везде...', '',
                                        '                                    Вы"']
                    elif type(view.field[position[0]][position[1]]) == Carrot:
                        message_text = ['Морковь:', '', '"Можно съесть...', '',
                                        '                                    Вы"']
                    elif type(view.field[position[0]][position[1]]) == Honey:
                        message_text = ['Мёд:', '', '"Ух ты, откуда же...', '',
                                        '                                    Вы"']
                    elif type(view.field[position[0]][position[1]]) == Mushroom:
                        message_text = ['Гриб:', '', '"Выглядит как гриб...', '',
                                        '                                    Вы"']
                    elif type(view.field[position[0]][position[1]]) == Berries:
                        message_text = ['Ягоды:', '', '"Хочу попробовать...', '',
                                        '                                    Вы"']
                    elif type(view.field[position[0]][position[1]]) == Hero:
                        message_text = ['"Да-да, это я...', '',
                                        '                                    Вы"']
                    elif type(view.field[position[0]][position[1]]) == NPS_1:
                        message_text = ['"Какой-то оборванец...', '',
                                        '                                    Вы"']
                    elif type(view.field[position[0]][position[1]]) == NPS_2:
                        message_text = ['"Красивая незнакомка...', '',
                                        '                                    Вы"']
                    elif type(view.field[position[0]][position[1]]) == Creator:
                        message_text = ['"Он прекрасен...', '',
                                        '                                    Вы"']

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if view.get_click(event.pos):
                        if type(view.field[view.get_cell(event.pos)[0]][
                                    view.get_cell(event.pos)[1]]) == Sticks or \
                                type(view.field[view.get_cell(event.pos)[0]][
                                         view.get_cell(event.pos)[1]]) == Stones or \
                                type(
                                    view.field[view.get_cell(event.pos)[0]][
                                        view.get_cell(event.pos)[1]]) == Grass or \
                                type(view.field[view.get_cell(event.pos)[0]][
                                         view.get_cell(event.pos)[1]]) == Brown_Stones or \
                                type(
                                    view.field[view.get_cell(event.pos)[0]][
                                        view.get_cell(event.pos)[1]]) == Brown_Grass or \
                                type(
                                    view.field[view.get_cell(event.pos)[0]][
                                        view.get_cell(event.pos)[1]]) == Carrot or \
                                type(
                                    view.field[view.get_cell(event.pos)[0]][
                                        view.get_cell(event.pos)[1]]) == Honey or \
                                type(
                                    view.field[view.get_cell(event.pos)[0]][
                                        view.get_cell(event.pos)[1]]) == Mushroom or \
                                type(
                                    view.field[view.get_cell(event.pos)[0]][view.get_cell(event.pos)[1]]) == Berries:
                            if len(inventory.get_inventory()) < 90:
                                object = type(
                                    view.field[view.get_cell(event.pos)[0]][
                                        view.get_cell(event.pos)[1]])
                                object_hp = object.get_hp(object)
                                weapon_power = hero.get_weapon()[1]
                                if object_hp > hero.get_weapon()[1]:
                                    object.set_hp(object, object_hp - weapon_power)
                                else:
                                    hero.take(view.get_board_cell(event.pos), event.pos)
                                    if object == Sticks:
                                        object.set_hp(object, sticks_hp)
                                    elif object == Stones:
                                        object.set_hp(object, stones_hp)
                                    elif object == Brown_Stones:
                                        object.set_hp(object, stones_hp)
                                    elif object == Grass:
                                        object.set_hp(object, grass_hp)
                                    elif object == Brown_Grass:
                                        object.set_hp(object, grass_hp)
                                    elif object == Carrot:
                                        object.set_hp(object, carrots_hp)
                                    elif object == Honey:
                                        object.set_hp(object, honey_hp)
                                    elif object == Mushroom:
                                        object.set_hp(object, mushroom_hp)
                                    elif object == Berries:
                                        object.set_hp(object, berries_hp)
                        elif type(view.field[view.get_cell(event.pos)[0]][view.get_cell(event.pos)[1]]) == NPS_1 or \
                                type(view.field[view.get_cell(event.pos)[0]][view.get_cell(event.pos)[1]]) == NPS_2 or \
                                type(view.field[view.get_cell(event.pos)[0]][view.get_cell(event.pos)[1]]) == Creator:
                            type(view.field[view.get_cell(event.pos)[0]][view.get_cell(event.pos)[1]]).start_dialog()
                        elif type(view.field[view.get_cell(event.pos)[0]][
                                      view.get_cell(event.pos)[1]]) == NPS_1 or \
                                type(view.field[view.get_cell(event.pos)[0]][
                                         view.get_cell(event.pos)[1]]) == NPS_2:
                            view.field[view.get_cell(event.pos)[0]][
                                view.get_cell(event.pos)[1]].start_dialog()
                    elif event.pos[0] > 880 and event.pos[1] <= 640:
                        try:
                            index = inventory.get_cell((event.pos[0] + 12, event.pos[1] + 6))
                            item = inventory.get_inventory()[index]
                        except Exception:
                            pass
                        if item == 'arm':
                            hero.set_weapon('arm', 2, index)
                        elif item == 'stick':
                            hero.set_weapon('stick', 3, index)
                        elif item == 'stone':
                            hero.set_weapon('stone', 4, index)
                        elif item == 'carrot':
                            hero.set_weapon('carrot', 0, index)
                        elif item == 'honey':
                            hero.set_weapon('honey', 0, index)
                        elif item == 'mushroom':
                            hero.set_weapon('mushroom', 0, index)
                        elif item == 'berries':
                            hero.set_weapon('berries', 0, index)
                elif event.button == 3:
                    if event.pos[0] > 880 and event.pos[1] <= 640:
                        index = inventory.get_cell((event.pos[0] + 12, event.pos[1] + 6))
                        item = inventory.get_inventory()[index]
                        if hero.get_weapon()[0] == item and hero.get_weapon()[2] == index:
                            if item == 'stick':
                                pass
                            elif item == 'stone':
                                pass
                            elif item == 'carrot':
                                inventory.delete_thing(index)
                                inventory_sticks.update('kill')
                                inventory_stones.update('kill')
                                inventory_honey.update('kill')
                                inventory_carrots.update('kill')
                                inventory_mushroom.update('kill')
                                inventory_berries.update('kill')
                                if hero.get_hunger() < 100:
                                    if hero.get_hunger() + 10 < 100:
                                        hero.set_hunger(hero.get_hunger() + 10)
                                    else:
                                        hero.set_hunger(100)
                                inventory.draw(0)
                            elif item == 'honey':
                                inventory.delete_thing(index)
                                inventory_sticks.update('kill')
                                inventory_stones.update('kill')
                                inventory_honey.update('kill')
                                inventory_carrots.update('kill')
                                inventory_mushroom.update('kill')
                                inventory_berries.update('kill')
                                if hero.get_hunger() < 100:
                                    if hero.get_hunger() + 15 < 100:
                                        hero.set_hunger(hero.get_hunger() + 15)
                                    else:
                                        hero.set_hunger(100)
                                inventory.draw(0)
                            elif item == 'mushroom':
                                inventory.delete_thing(index)
                                inventory_sticks.update('kill')
                                inventory_stones.update('kill')
                                inventory_honey.update('kill')
                                inventory_carrots.update('kill')
                                inventory_mushroom.update('kill')
                                inventory_berries.update('kill')
                                if hero.get_hunger() < 100:
                                    if hero.get_hunger() + 10 < 100:
                                        hero.set_hunger(hero.get_hunger() + 10)
                                    else:
                                        hero.set_hunger(100)
                                inventory.draw(0)
                            elif item == 'berries':
                                inventory.delete_thing(index)
                                inventory_sticks.update('kill')
                                inventory_stones.update('kill')
                                inventory_honey.update('kill')
                                inventory_carrots.update('kill')
                                inventory_mushroom.update('kill')
                                inventory_berries.update('kill')
                                if hero.get_hunger() < 100:
                                    if hero.get_hunger() + 5 < 100:
                                        hero.set_hunger(hero.get_hunger() + 5)
                                    else:
                                        hero.set_hunger(100)
                                inventory.draw(0)

        # Вывод сообщений
        message_clock += 2
        if message_clock >= 1000 and message_text == []:
            random_phrase = random.randrange(-1, 3)
            message_text = list_of_messages[random_phrase]
            passive_text = message_text
        if passive_text == message_text:
            if message_clock >= 1250:
                message_text = []
                message_clock = 0
        elif message_text:
            if message_clock >= 750:
                message_text = []
                message_clock = 0

        # Запуск музыки
        music_time += 1
        fon_time += 1
        if fon_time == 1:
            if location == 'forest':
                stop_music(rain_audio)
                play_music(birds_audio)
            elif location == 'rainy-dale':
                stop_music(birds_audio)
                play_music(rain_audio)
            elif location == 'dark-forest':
                stop_music(rain_audio)
        if fon_time == 1000:
            fon_time = 0
        if music_time == 5000:
            play_music(mus)
        if 1000 < music_time < 2000:
            if volume < 1:
                volume += 0.001
                volume_music(mus, volume)
        if music_time >= 8000:
            volume -= 0.001
            print(volume)
            volume_music(mus, volume)
            if volume <= 0:
                stop_music(mus)
                music_time = 0
                volume = 0
                if mus == fon_1:
                    mus = fon_2
                else:
                    mus = fon_1

        # Отрисовка объектов
        for sprite in all_sticks:
            all_sticks.update(True, (sprite.rect.x, sprite.rect.y))
        for sprite in all_stones:
            all_stones.update(True, (sprite.rect.x, sprite.rect.y))
        for sprite in all_grass:
            all_grass.update(True, (sprite.rect.x, sprite.rect.y))
        for sprite in all_brown_stones:
            all_brown_stones.update(True, (sprite.rect.x, sprite.rect.y))
        for sprite in all_brown_grass:
            all_brown_grass.update(True, (sprite.rect.x, sprite.rect.y))
        for sprite in all_dark_grass:
            all_dark_grass.update(True, (sprite.rect.x, sprite.rect.y))
        for sprite in all_blue_fire:
            all_blue_fire.update(True, (sprite.rect.x, sprite.rect.y))

        for sprite in all_carrot:
            all_carrot.update(True, (sprite.rect.x, sprite.rect.y))
        for sprite in all_honey:
            all_honey.update(True, (sprite.rect.x, sprite.rect.y))
        for sprite in all_mushrooms:
            all_mushrooms.update(True, (sprite.rect.x, sprite.rect.y))
        for sprite in all_berries:
            all_berries.update(True, (sprite.rect.x, sprite.rect.y))

        for sprite in npc_1_sprite:
            npc_1_sprite.update(True, (sprite.rect.x, sprite.rect.y))
        for sprite in npc_2_sprite:
            npc_2_sprite.update(True, (sprite.rect.x, sprite.rect.y))
        for sprite in creator_sprite:
            creator_sprite.update(True, (sprite.rect.x, sprite.rect.y))
        hero_sprite.update(hero)

        all_sticks.draw(screen)
        all_stones.draw(screen)
        all_grass.draw(screen)
        all_brown_grass.draw(screen)
        all_brown_stones.draw(screen)
        all_dark_grass.draw(screen)
        all_blue_fire.draw(screen)
        inventory_arm.draw(screen)
        inventory_sticks.draw(screen)
        inventory_stones.draw(screen)
        inventory_carrots.draw(screen)
        inventory_honey.draw(screen)
        inventory_mushroom.draw(screen)
        inventory_berries.draw(screen)

        all_carrot.draw(screen)
        all_honey.draw(screen)
        all_mushrooms.draw(screen)
        all_berries.draw(screen)

        hero_sprite.draw(screen)
        npc_1_sprite.draw(screen)
        npc_2_sprite.draw(screen)
        creator_sprite.draw(screen)
        print_text(text_coord, message_text)

        # Отрисовка декораций
        decoration_clock += 1
        random_decoration = random.randrange(0, 10)
        x = random.randrange(0, 20)
        y = random.randrange(0, 20)
        if location == 'forest':
            if random_decoration > 1 and decoration_clock == 500:
                D_butterfly((x, y), d_butterfly_sprite)
            if decoration_clock > 500:
                decoration_clock = 0
        elif location == 'rainy-dale':
            if decoration_clock == 1:
                D_rain((x, 0), d_rain_sprite)
                D_rain((x + 2, y), d_rain_sprite)
            if decoration_clock > 1:
                decoration_clock = 0
        elif location == 'dark-forest':
            if decoration_clock % 30 == 0:
                for sprite in all_dark_grass:
                    flag = random.randint(0, 1)
                    if flag:
                        all_dark_grass.update('animation', (sprite.rect.x, sprite.rect.y))
                for sprite in all_blue_fire:
                    flag = random.randint(0, 1)
                    if flag:
                        all_blue_fire.update('animation', (sprite.rect.x, sprite.rect.y))

        for sprite in d_butterfly_sprite:
            d_butterfly_sprite.update(True, (sprite.rect.x, sprite.rect.y))
        for sprite in d_rain_sprite:
            d_rain_sprite.update(True, (sprite.rect.x, sprite.rect.y))

        d_butterfly_sprite.update('animation', None)
        d_rain_sprite.update('animation', None)
        d_butterfly_sprite.draw(screen)
        d_rain_sprite.draw(screen)

        if pygame.mouse.get_focused():
            pygame.mouse.set_visible(False)
            arrow_sprite.draw(screen)
        screen.blit(text_hunger, text_hunger_rect)
        screen.blit(text_hp, text_hp_rect)
        pygame.display.flip()
        clock.tick(FPS)

    update_level(level)
    cur.execute(f"""UPDATE level SET level = '{level}'""")
    cur.execute(f"""UPDATE hp SET hp = '{hero.get_hp()}'""")
    cur.execute(f"""UPDATE hunger SET hunger = '{hero.get_hunger()}'""")
    cur.execute(f"""DELETE FROM inventory WHERE thing = 'stick' or thing = 'stone' or 
    thing = 'carrot' or thing = 'honey' or thing = 'mushroom' or thing = 'berries'""")
    for i in range(len(inventory.get_inventory())):
        if i != 0:
            cur.execute(f"""INSERT INTO inventory(thing) 
            VALUES ('{inventory.get_inventory()[i]}')""")
    con.commit()
    con.close()
    pygame.quit()
