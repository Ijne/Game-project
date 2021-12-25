import pygame
import os
import sys
import random

# Готовим игру к работе
pygame.init()
screen = pygame.display.set_mode((1180, 880))
clock = pygame.time.Clock()
FPS = 60


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


# Функции загрузочного экрана
def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


# Загрузка уровня
def load_level(filename):
    filename = 'data/levels/' + filename
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
    if level == 'level_1.txt':
        if arg == pygame.K_w:
            return 'level_2.txt'
        elif arg == pygame.K_s:
            return 'level_3.txt'
        elif arg == pygame.K_a:
            return 'level_4.txt'
        elif arg == pygame.K_d:
            return 'level_5.txt'
    elif level == 'level_2.txt':
        if arg == pygame.K_w:
            return False
        elif arg == pygame.K_s:
            return 'level_1.txt'
        elif arg == pygame.K_a:
            return 'level_8.txt'
        elif arg == pygame.K_d:
            return 'level_9.txt'
    elif level == 'level_3.txt':
        if arg == pygame.K_w:
            return 'level_1.txt'
        elif arg == pygame.K_s:
            return False
        elif arg == pygame.K_a:
            return 'level_7.txt'
        elif arg == pygame.K_d:
            return 'level_6.txt'
    elif level == 'level_4.txt':
        if arg == pygame.K_w:
            return 'level_8.txt'
        elif arg == pygame.K_s:
            return 'level_7.txt'
        elif arg == pygame.K_a:
            return False
        elif arg == pygame.K_d:
            return 'level_1.txt'
    elif level == 'level_5.txt':
        if arg == pygame.K_w:
            return 'level_9.txt'
        elif arg == pygame.K_s:
            return 'level_6.txt'
        elif arg == pygame.K_a:
            return 'level_1.txt'
        elif arg == pygame.K_d:
            return False
    elif level == 'level_6.txt':
        if arg == pygame.K_w:
            return 'level_5.txt'
        elif arg == pygame.K_s:
            return False
        elif arg == pygame.K_a:
            return 'level_3.txt'
        elif arg == pygame.K_d:
            return False
    elif level == 'level_7.txt':
        if arg == pygame.K_w:
            return 'level_4.txt'
        elif arg == pygame.K_s:
            return False
        elif arg == pygame.K_a:
            return False
        elif arg == pygame.K_d:
            return 'level_3.txt'
    elif level == 'level_8.txt':
        if arg == pygame.K_w:
            return False
        elif arg == pygame.K_s:
            return 'level_4.txt'
        elif arg == pygame.K_a:
            return False
        elif arg == pygame.K_d:
            return 'level_2.txt'
    elif level == 'level_9.txt':
        if arg == pygame.K_w:
            return False
        elif arg == pygame.K_s:
            return 'level_5.txt'
        elif arg == pygame.K_a:
            return 'level_2.txt'
        elif arg == pygame.K_d:
            return False


# Функция загрузки нового уровня
def reload_level(new_level):
    global level, hero
    if new_level:
        generate_level(load_level(new_level))
        level = new_level

        # Создание спрайтов
        all_sticks.update(False, None)
        all_stones.update(False, None)
        all_grass.update(False, None)
        hero_sprite.update(False)
        npc_1_sprite.update(False)

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
                elif board.field[x][y] == '1':
                    element = NPS_1((x, y))
                    board.field[x][y] = element
                    NPS_1_Image(element, npc_1_sprite)
        flag = False
        for x in range(len(board.field[:8])):
            if flag:
                break
            for y in range(len(board.field[x])):
                if board.field[x][y] == 0:
                    hero = Hero((x, y))
                    board.field[x][y] = hero
                    Hero_image(hero, hero_sprite)
                    hero_sprite.update(hero)
                    flag = True
                    break


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
            elif type(board.field[x][y]) == Hero:
                s += '0'
            elif type(board.field[x][y]) == NPS_1:
                s += '1'
        output.append(s + '\n')

    filename = 'data/levels/' + level
    with open(filename, 'w') as mapFile:
        mapFile.writelines(output)


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


# Классы палок
class Sticks_image(pygame.sprite.Sprite):
    image = load_image('sticks.png')

    def __init__(self, stick, *group):
        super().__init__(*group)
        self.image = Sticks_image.image
        self.rect = self.image.get_rect()
        self.rect.x = stick.position[0] * board.cell_size + board.left
        self.rect.y = stick.position[1] * board.cell_size + board.top

    def update(self, arg, position):
        global message_text
        if not arg:
            self.kill()
        if arg and self.rect.collidepoint(position):
            if arg == 'kill':
                message_text = ['"Полезная штука...', '',
                                '                                    Ваня"']
                self.kill()


class Sticks:
    def __init__(self, position, number):
        self.number = number
        self.position = position
        self.power = 0


# Классы камней
class Stones_image(pygame.sprite.Sprite):
    image = load_image('stones.png')

    def __init__(self, stone, *group):
        super().__init__(*group)
        self.image = Stones_image.image
        self.rect = self.image.get_rect()
        self.rect.x = stone.position[0] * board.cell_size + board.left
        self.rect.y = stone.position[1] * board.cell_size + board.top

    def update(self, arg, position):
        global message_text
        if not arg:
            self.kill()
        if arg and self.rect.collidepoint(position):
            if arg == 'kill':
                message_text = ['"Как мне их тоскать...', '',
                                '                                    Ваня"']
                self.kill()


class Stones:
    def __init__(self, position, number):
        self.number = number
        self.position = position
        self.power = 10


# Классы травы
class Grass_image(pygame.sprite.Sprite):
    image = load_image('grass.png')

    def __init__(self, grass, *group):
        super().__init__(*group)
        self.image = Grass_image.image
        self.rect = self.image.get_rect()
        self.rect.x = grass.position[0] * board.cell_size + board.left
        self.rect.y = grass.position[1] * board.cell_size + board.top

    def update(self, arg, position):
        global message_text
        if not arg:
            self.kill()
        if arg and self.rect.collidepoint(position):
            if arg == 'kill':
                message_text = ['"Травка...', '',
                                '                                    Ваня"']
                self.kill()


class Grass:
    def __init__(self, position, number):
        self.number = number
        self.position = position
        self.power = 0


# Классы героя
class Hero_image(pygame.sprite.Sprite):
    image_90 = load_image('hero_90.png')
    image_0 = load_image('hero_0.png')
    image_180 = load_image('hero_180.png')

    def __init__(self, hero, *group):
        super().__init__(*group)
        self.image = Hero_image.image_90
        self.rect = self.image.get_rect()
        self.rect.x = hero.position[0] * board.cell_size + board.left
        self.rect.y = hero.position[1] * board.cell_size + board.top

    def update(self, hero, *args):
        if not hero:
            self.kill()
        else:
            self.image = Hero_image.image_90
            self.rect.x = hero.position[0] * board.cell_size + board.left
            self.rect.y = hero.position[1] * board.cell_size + board.top
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

    def move(self, arg):
        if arg == pygame.K_w:
            if board.field[self.position[0]][self.position[1] - 1] == 0 and \
                    board.on_click((self.position[0], self.position[1] - 1)):
                self.position = (self.position[0], self.position[1] - 1)
                self.view = 0
                board.field[hero.position[0]][hero.position[1] + 1] = 0
                board.field[self.position[0]][self.position[1]] = self
                hero_sprite.update(self)
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
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                                process = False
                            elif event.type == pygame.QUIT:
                                update_level(level)
                                pygame.quit()

                        # Отрисовка объектов
                        all_sticks.draw(screen)
                        all_stones.draw(screen)
                        all_grass.draw(screen)
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
                hero_sprite.update(self)
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
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                                process = False
                            elif event.type == pygame.QUIT:
                                update_level(level)
                                pygame.quit()

                        # Отрисовка объектов
                        all_sticks.draw(screen)
                        all_stones.draw(screen)
                        all_grass.draw(screen)
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
                hero_sprite.update(self)
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
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                                process = False
                            elif event.type == pygame.QUIT:
                                update_level(level)
                                pygame.quit()

                        # Отрисовка объектов
                        all_sticks.draw(screen)
                        all_stones.draw(screen)
                        all_grass.draw(screen)
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
                hero_sprite.update(self)
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
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                                process = False
                            elif event.type == pygame.QUIT:
                                update_level(level)
                                pygame.quit()

                        # Отрисовка объектов
                        all_sticks.draw(screen)
                        all_stones.draw(screen)
                        all_grass.draw(screen)
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
                            board.field[position[0]][position[1]] = 0
                            all_sticks.update('kill', rect_position)
                            all_stones.update('kill', rect_position)
                            all_grass.update('kill', rect_position)


# НПС-Оборванец
class NPS_1_Image(pygame.sprite.Sprite):
    image = load_image('npc-1.png')

    def __init__(self, npc, *group):
        super().__init__(*group)
        self.image = NPS_1_Image.image
        self.rect = self.image.get_rect()
        self.rect.x = npc.position[0] * board.cell_size + board.left
        self.rect.y = npc.position[1] * board.cell_size + board.top

    def update(self, arg):
        if not arg:
            self.kill()


class NPS_1:
    def __init__(self, position):
        self.position = position
        self.name = 'Оборванец'
        self.questions = [('-Кто ты?', '-Кто ты?'), ('-Что ты здесь делаешь?', '-Что ты здесь делаешь?'),
                          ('-Давно ты тут?', '-Давно ты тут?'), ('-Нам больше не о чем говорить',
                                                                 '-Я не хочу с тобой говорить')]
        self.answers = [('Пусто', 'Пусто'), ('-Приятно познакомиться', '-Я и сам не знаю'),
                        ('-Чтож, я тоже', '-Будь менее грубым'), ('-Пока', '-Иди')]
        self.hero_answers = [('E - Я Ваня', 'F - Скажи кто ты'), ('E - Я даже не знаю где я', 'F - Не твоё дело'),
                             ('E - Только очнулся', 'F - Не знаю'), ('E - Пока', 'F - Я ухожу')]
        self.step = 0
        self.feel = 0

    def start_dialog(self):
        process = True
        while process:
            screen.blit(background, (0, 0))
            screen.blit(second_menu_background, (880, 640))
            screen.blit(inventory_menu_background, (880, 0))
            if 0 < self.step <= len(self.questions) - 1:
                message_text = ['Оборванец:', '', self.answers[self.step][self.feel], '',
                                self.questions[self.step][self.feel], '',
                                self.hero_answers[self.step][0], '', self.hero_answers[self.step][1]]
            else:
                message_text = ['Оборванец:', '', self.questions[self.step][self.feel], '',
                                self.hero_answers[self.step][0], '', self.hero_answers[self.step][1]]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_e and self.step <= len(self.answers) - 1:
                    message_text = ['Оборванец:', '', self.answers[self.step][0], '',
                                    'Оборванец:', self.questions[self.step][self.feel], '',
                                    self.hero_answers[self.step][0], '', self.hero_answers[self.step][1]
                                    ]
                    self.step += 1
                    self.feel = 0
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_f and self.step <= len(self.answers) - 1:
                    message_text = ['Оборванец:', self.answers[self.step][1], '',
                                    'Оборванец:', self.questions[self.step][self.feel], '',
                                    self.hero_answers[self.step][0], '', self.hero_answers[self.step][1]
                                    ]
                    self.step += 1
                    self.feel = 1
                elif self.step > len(self.answers) - 1:
                    self.step = 0
                    self.feel = 0
                    process = False
                if event.type == pygame.MOUSEMOTION:
                    arrow.rect.x = event.pos[0]
                    arrow.rect.y = event.pos[1]

            # Отрисовка объектов
            all_sticks.draw(screen)
            all_stones.draw(screen)
            all_grass.draw(screen)
            hero_sprite.draw(screen)
            npc_1_sprite.draw(screen)
            print_text(text_coord, message_text)
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
        for i in range(self.width):
            for j in range(self.height):
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


# Запуск
if __name__ == '__main__':
    # Заставка
    start_screen()

    # Генерация уровня
    board = Board(20, 20, screen)
    generate_level(load_level('level_1.txt'))
    level = 'level_1.txt'
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
    hero_sprite = pygame.sprite.Group()
    npc_1_sprite = pygame.sprite.Group()

    # Текст
    message_text = []

    font = pygame.font.Font(None, 25)
    text_coord = (910, 670)

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
            elif board.field[x][y] == '1':
                element = NPS_1((x, y))
                board.field[x][y] = element
                NPS_1_Image(element, npc_1_sprite)
    flag = False
    for x in range(len(board.field[:8])):
        if flag:
            break
        for y in range(len(board.field[x])):
            if board.field[x][y] == 0:
                hero = Hero((x, y))
                board.field[x][y] = hero
                Hero_image(hero, hero_sprite)
                flag = True
                break

    # Непосредственно запуск
    running = True
    while running:
        if level == 'level_1.txt' or level == 'level_8.txt' or level == 'level_6.txt':
            background = pygame.transform.scale(load_image('background-field(2).png'), (880, 880))
        else:
            background = pygame.transform.scale(load_image('background-field.png'), (880, 880))
        screen.blit(background, (0, 0))
        screen.blit(second_menu_background, (880, 640))
        screen.blit(inventory_menu_background, (880, 0))
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
                        hero.move(event.key)
            if event.type == pygame.MOUSEMOTION:
                arrow.rect.x = event.pos[0]
                arrow.rect.y = event.pos[1]
                if board.get_click(event.pos):
                    position = board.get_cell(event.pos)
                    if type(board.field[position[0]][position[1]]) == Sticks:
                        message_text = ['Палки:', '', '"Хотя бы что-то...', '',
                                        '                                    Ваня"']
                    elif type(board.field[position[0]][position[1]]) == Stones:
                        message_text = ['Обычный камень:', '', '"Пфф, ничего не обычного...', '',
                                        '                                    Ваня"']
                    elif type(board.field[position[0]][position[1]]) == Grass:
                        message_text = ['Зелёная трава:', '', '"В хозяйстве пригодиться...', '',
                                        '                                    Ваня"']
                    elif type(board.field[position[0]][position[1]]) == Hero:
                        message_text = ['"Да-да, это я...', '',
                                        '                                    Ваня"']
                    elif type(board.field[position[0]][position[1]]) == NPS_1:
                        message_text = ['"Какой-то оборванец...', '',
                                        '                                    Ваня"']
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if board.get_click(event.pos):
                        if type(board.field[board.get_cell(event.pos)[0]][board.get_cell(event.pos)[1]]) == Sticks or \
                                type(board.field[board.get_cell(event.pos)[0]][
                                         board.get_cell(event.pos)[1]]) == Stones or \
                                type(board.field[board.get_cell(event.pos)[0]][board.get_cell(event.pos)[1]]) == Grass:
                            hero.take(board.get_cell(event.pos), event.pos)
                        elif type(board.field[board.get_cell(event.pos)[0]][board.get_cell(event.pos)[1]]) == NPS_1:
                            board.field[board.get_cell(event.pos)[0]][board.get_cell(event.pos)[1]].start_dialog()

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

        # Отрисовка объектов
        all_sticks.draw(screen)
        all_stones.draw(screen)
        all_grass.draw(screen)
        hero_sprite.draw(screen)
        npc_1_sprite.draw(screen)
        print_text(text_coord, message_text)
        if pygame.mouse.get_focused():
            pygame.mouse.set_visible(False)
            arrow_sprite.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    update_level(level)
    pygame.quit()
