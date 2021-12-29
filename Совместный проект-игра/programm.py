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
    filename = 'data/levels/default/' + filename
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
    global level, hero, location
    if new_level:
        generate_level(load_level(new_level))
        level = new_level
        x = level[level.find('(') + 1:level.find(',')].strip()
        y = level[level.find(',') + 1:level.find(')')].strip()

        if int(x) < -4 or int(x) > 4 or int(y) < -4 or int(y) > 4:
            location = 'brown-field'
        else:
            location = 'forest'

        print(location)

        # Создание спрайтов
        all_sticks.update(False, None)
        all_stones.update(False, None)
        all_grass.update(False, None)
        all_brown_grass.update(False, None)
        all_brown_stones.update(False, None)

        all_carrot.update(False, None)
        all_honey.update(False, None)
        all_mushrooms.update(False, None)
        all_berries.update(False, None)

        npc_1_sprite.update(False, None)
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
        output.append(s + '\n')

    filename = 'data/levels/default/' + level
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
        else:
            if self.rect.x > 800 or self.rect.x < 40 or self.rect.y > 800 or self.rect.y < 40:
                if self.rect.collidepoint(position):
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
    image = pygame.transform.scale(load_image('stones.png'), (43, 43))

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
        else:
            if self.rect.x > 800 or self.rect.x < 40 or self.rect.y > 800 or self.rect.y < 40:
                if self.rect.collidepoint(position):
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
    def __init__(self, position, number):
        self.number = number
        self.position = position
        self.power = 0


# Классы коричневых камней
class Browns_Stones_image(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('stones-brown.png'), (43, 43))

    def __init__(self, stone, *group):
        super().__init__(*group)
        self.image = Browns_Stones_image.image
        self.rect = self.image.get_rect()
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
                    self.kill()


class Brown_Stones:
    def __init__(self, position, number):
        self.number = number
        self.position = position
        self.power = 10


# Классы коричневой травы
class Borwn_Grass_image(pygame.sprite.Sprite):
    image = load_image('grass-brown.png')

    def __init__(self, grass, *group):
        super().__init__(*group)
        self.image = Borwn_Grass_image.image
        self.rect = self.image.get_rect()
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
    def __init__(self, position, number):
        self.number = number
        self.position = position
        self.power = 0


# Классы морковки
class Carrot_image(pygame.sprite.Sprite):
    image = load_image('carrot.png')

    def __init__(self, carrot, *group):
        super().__init__(*group)
        self.image = Carrot_image.image
        self.rect = self.image.get_rect()
        self.rect.x = carrot.position[0] * board.cell_size + board.left
        self.rect.y = carrot.position[1] * board.cell_size + board.top

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
                    message_text = ['"Отличная морковь...', '',
                                    '                                    Ваня"']
                    self.kill()


class Carrot:
    def __init__(self, position):
        self.food = 10
        self.position = position


# Классы ульев
class Honey_image(pygame.sprite.Sprite):
    image = load_image('honey.png')

    def __init__(self, honey, *group):
        super().__init__(*group)
        self.image = Honey_image.image
        self.rect = self.image.get_rect()
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
                    self.kill()


class Honey:
    def __init__(self, position):
        self.food = 20
        self.position = position


# Классы грибов
class Mushroom_image(pygame.sprite.Sprite):
    image = load_image('mushroom.png')

    def __init__(self, mushroom, *group):
        super().__init__(*group)
        self.image = Mushroom_image.image
        self.rect = self.image.get_rect()
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
                    self.kill()


class Mushroom:
    def __init__(self, position):
        self.food = 20
        self.position = position


# Классы ягод
class Berries_image(pygame.sprite.Sprite):
    image = load_image('berries.png')

    def __init__(self, berries, *group):
        super().__init__(*group)
        self.image = Berries_image.image
        self.rect = self.image.get_rect()
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
                    self.kill()


class Berries:
    def __init__(self, position):
        self.food = 30
        self.position = position


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

    def move(self, arg):
        if arg == pygame.K_w:
            if board.field[self.position[0]][self.position[1] - 1] == 0 and \
                    board.on_click((self.position[0], self.position[1] - 1)):
                self.position = (self.position[0], self.position[1] - 1)
                self.view = 0
                board.field[hero.position[0]][hero.position[1] + 1] = 0
                board.field[self.position[0]][self.position[1]] = self
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
                                pygame.quit()

                        # Отрисовка объектов
                        all_sticks.draw(screen)
                        all_stones.draw(screen)
                        all_grass.draw(screen)
                        all_brown_grass.draw(screen)
                        all_brown_stones.draw(screen)

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
                                pygame.quit()

                        # Отрисовка объектов
                        all_sticks.draw(screen)
                        all_stones.draw(screen)
                        all_grass.draw(screen)
                        all_brown_grass.draw(screen)
                        all_brown_stones.draw(screen)

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
                                pygame.quit()

                        # Отрисовка объектов
                        all_sticks.draw(screen)
                        all_stones.draw(screen)
                        all_grass.draw(screen)
                        all_brown_grass.draw(screen)
                        all_brown_stones.draw(screen)

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
                                pygame.quit()

                        # Отрисовка объектов
                        all_sticks.draw(screen)
                        all_stones.draw(screen)
                        all_grass.draw(screen)
                        all_brown_grass.draw(screen)
                        all_brown_stones.draw(screen)

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
                            board.field[position[0]][position[1]] = 0
                            view.field[position[0] - top[0]][position[1] - top[1]] = 0
                            all_sticks.update('kill', rect_position)
                            all_stones.update('kill', rect_position)
                            all_grass.update('kill', rect_position)
                            all_brown_grass.update('kill', rect_position)
                            all_brown_grass.update('kill', rect_position)

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
                process = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
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


# Класс инвентаря
class Inventory:
    def __init__(self):
        self.inventory = []

    def get_inventory(self):
        return self.inventory

    def add_thing(self, thing):
        self.inventory.append(thing)

    def delete_thing(self, thing):
        n = self.inventory.index(thing)
        del self.inventory[n]


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


# Запуск
if __name__ == '__main__':
    # Заставка
    start_screen()

    # Генерация уровня
    board = Board(30, 30, screen)
    view = View()
    location = 'forest'

    generate_level(load_level('level(0, 0).txt'))
    level = 'level(0, 0).txt'

    camera = Camera()
    top = (0, 0)
    bottom = (19, 19)

    nps_1_step = 1

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

    all_carrot = pygame.sprite.Group()
    all_honey = pygame.sprite.Group()
    all_mushrooms = pygame.sprite.Group()
    all_berries = pygame.sprite.Group()

    hero_sprite = pygame.sprite.Group()
    npc_1_sprite = pygame.sprite.Group()

    # Спрайты декораций
    d_butterfly_sprite = pygame.sprite.Group()

    # Текст
    message_text = []

    font = pygame.font.Font(None, 25)
    text_coord = (910, 670)

    # Стартовые инструменты
    inventory = Inventory()
    arm = Weapon(2, 2)
    inventory.add_thing(arm)
    stick = Weapon(4, 4)
    inventory.add_thing(stick)

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

    # Непосредственно запуск
    running = True
    while running:
        if location == 'forest':
            background = pygame.transform.scale(load_image('background-field.png'), (880, 880))
        elif location == 'brown-field':
            background = pygame.transform.scale(load_image('background-brown.png'), (880, 880))
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

                            all_carrot.update(False, None)
                            all_honey.update(False, None)
                            all_mushrooms.update(False, None)
                            all_berries.update(False, None)

                            npc_1_sprite.update(False, None)

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

            if event.type == pygame.MOUSEMOTION:
                arrow.rect.x = event.pos[0]
                arrow.rect.y = event.pos[1]
                if view.get_click(event.pos):
                    position = view.get_cell(event.pos)
                    if type(view.field[position[0]][position[1]]) == Sticks:
                        message_text = ['Палки:', '', '"Хотя бы что-то...', '',
                                        '                                    Ваня"']
                    elif type(view.field[position[0]][position[1]]) == Stones:
                        message_text = ['Обычный камень:', '', '"Пфф, ничего не обычного...', '',
                                        '                                    Ваня"']
                    elif type(view.field[position[0]][position[1]]) == Grass:
                        message_text = ['Зелёная трава:', '', '"В хозяйстве пригодиться...', '',
                                        '                                    Ваня"']
                    elif type(view.field[position[0]][position[1]]) == Brown_Grass:
                        message_text = ['Жёлтая трава:', '', '"От неё идёт запах...', '',
                                        '                                    Ваня"']
                    elif type(view.field[position[0]][position[1]]) == Brown_Stones:
                        message_text = ['Малый камень:', '', '"Камень, как и везде...', '',
                                        '                                    Ваня"']
                    elif type(view.field[position[0]][position[1]]) == Carrot:
                        message_text = ['Морковь:', '', '"Можно съесть...', '',
                                        '                                    Ваня"']
                    elif type(view.field[position[0]][position[1]]) == Honey:
                        message_text = ['Мёд:', '', '"Ух ты, откуда же...', '',
                                        '                                    Ваня"']
                    elif type(view.field[position[0]][position[1]]) == Mushroom:
                        message_text = ['Гриб:', '', '"Выглядит как гриб...', '',
                                        '                                    Ваня"']
                    elif type(view.field[position[0]][position[1]]) == Berries:
                        message_text = ['Ягоды:', '', '"Хочу попробовать...', '',
                                        '                                    Ваня"']
                    elif type(view.field[position[0]][position[1]]) == Hero:
                        message_text = ['"Да-да, это я...', '',
                                        '                                    Ваня"']
                    elif type(view.field[position[0]][position[1]]) == NPS_1:
                        message_text = ['"Какой-то оборванец...', '',
                                        '                                    Ваня"']
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if view.get_click(event.pos):
                        if type(view.field[view.get_cell(event.pos)[0]][view.get_cell(event.pos)[1]]) == Sticks or \
                                type(view.field[view.get_cell(event.pos)[0]][
                                         view.get_cell(event.pos)[1]]) == Stones or \
                                type(
                                    view.field[view.get_cell(event.pos)[0]][view.get_cell(event.pos)[1]]) == Grass or \
                                type(view.field[view.get_cell(event.pos)[0]][
                                         view.get_cell(event.pos)[1]]) == Brown_Stones or \
                                type(
                                    view.field[view.get_cell(event.pos)[0]][
                                        view.get_cell(event.pos)[1]]) == Brown_Grass or \
                                type(
                                    view.field[view.get_cell(event.pos)[0]][view.get_cell(event.pos)[1]]) == Carrot or \
                                type(
                                    view.field[view.get_cell(event.pos)[0]][view.get_cell(event.pos)[1]]) == Honey or \
                                type(
                                    view.field[view.get_cell(event.pos)[0]][
                                        view.get_cell(event.pos)[1]]) == Mushroom or \
                                type(
                                    view.field[view.get_cell(event.pos)[0]][view.get_cell(event.pos)[1]]) == Berries:
                            hero.take(view.get_board_cell(event.pos), event.pos)
                        elif type(view.field[view.get_cell(event.pos)[0]][view.get_cell(event.pos)[1]]) == NPS_1:
                            view.field[view.get_cell(event.pos)[0]][view.get_cell(event.pos)[1]].start_dialog()

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
        hero_sprite.update(hero)

        all_sticks.draw(screen)
        all_stones.draw(screen)
        all_grass.draw(screen)
        all_brown_grass.draw(screen)
        all_brown_stones.draw(screen)

        all_carrot.draw(screen)
        all_honey.draw(screen)
        all_mushrooms.draw(screen)
        all_berries.draw(screen)

        hero_sprite.draw(screen)
        npc_1_sprite.draw(screen)
        print_text(text_coord, message_text)

        # Отрисовка декораций
        decoration_clock += 1
        random_decoration = random.randrange(0, 10)
        x = random.randrange(0, 20)
        y = random.randrange(0, 20)
        if random_decoration > 1 and decoration_clock == 500:
            D_butterfly((x, y), d_butterfly_sprite)
        if decoration_clock > 500:
            decoration_clock = 0

        for sprite in d_butterfly_sprite:
            d_butterfly_sprite.update(True, (sprite.rect.x, sprite.rect.y))

        d_butterfly_sprite.update('animation', None)
        d_butterfly_sprite.draw(screen)

        if pygame.mouse.get_focused():
            pygame.mouse.set_visible(False)
            arrow_sprite.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    update_level(level)
    pygame.quit()
