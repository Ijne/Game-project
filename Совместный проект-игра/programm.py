import pygame
import os
import sys
import random

# Готовим игру к работе
pygame.init()
screen = pygame.display.set_mode((880, 880))
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
        if arg and self.rect.collidepoint(position):
            pass
        elif not arg and self.rect.collidepoint(position):
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
        if arg and self.rect.collidepoint(position):
            pass
        elif not arg and self.rect.collidepoint(position):
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
        if arg and self.rect.collidepoint(position):
            pass
        elif not arg and self.rect.collidepoint(position):
            self.kill()


class Grass:
    def __init__(self, position, number):
        self.number = number
        self.position = position
        self.power = 0


# Классы героя
class Hero_image(pygame.sprite.Sprite):
    image = load_image('hero.png')

    def __init__(self, hero, *group):
        super().__init__(*group)
        self.image = Hero_image.image
        self.rect = self.image.get_rect()
        self.rect.x = hero.position[0] * board.cell_size + board.left
        self.rect.y = hero.position[1] * board.cell_size + board.top

    def update(self, hero, *args):
        self.image = Hero_image.image
        self.rect.x = hero.position[0] * board.cell_size + board.left
        self.rect.y = hero.position[1] * board.cell_size + board.top
        if hero.view == 0:
            self.image = pygame.transform.rotate(self.image, 90)
            hero.view = 0
        elif hero.view == 270:
            self.image = pygame.transform.rotate(self.image, 180)
            hero.view = 270
        elif hero.view == 180:
            self.image = pygame.transform.rotate(self.image, -90)
            hero.view = 180


class Hero:
    def __init__(self, position):
        self.hp = 100
        self.position = position
        self.view = 90

    def move(self, arg):
        if arg.key == pygame.K_w:
            if board.field[self.position[0]][self.position[1] - 1] == 0 and \
                    board.on_click((self.position[0], self.position[1] - 1)):
                self.position = (self.position[0], self.position[1] - 1)
                self.view = 0
        elif arg.key == pygame.K_s:
            if board.on_click((self.position[0], self.position[1] + 1)) and \
                    board.field[self.position[0]][self.position[1] + 1] == 0:
                self.position = (self.position[0], self.position[1] + 1)
                self.view = 180
        elif arg.key == pygame.K_a:
            if board.field[self.position[0] - 1][self.position[1]] == 0 and \
                    board.on_click((self.position[0] - 1, self.position[1])):
                self.position = (self.position[0] - 1, self.position[1])
                self.view = 270
        elif arg.key == pygame.K_d:
            if board.on_click((self.position[0] + 1, self.position[1])) and \
                    board.field[self.position[0] + 1][self.position[1]] == 0:
                self.position = (self.position[0] + 1, self.position[1])
                self.view = 90
        hero_sprite.update(self)

    def rotate(self, arg):
        if arg.key == pygame.K_w:
            self.view = 0
        elif arg.key == pygame.K_s:
            self.view = 180
        elif arg.key == pygame.K_a:
            self.view = 270
        elif arg.key == pygame.K_d:
            self.view = 90
        hero_sprite.update(self)


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

# класс инвенторя
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

# класс инструментов
class Weapon:
    def __init__(self, power, damage):
        self.power = power
        self.damage = damage

    def get_power(self):
        return self.power

    def get_damage(self):
        return self.damage


# Запуск
if __name__ == '__main__':
    # Заставка
    start_screen()

    # Генерация уровня
    board = Board(20, 20, screen)
    background = pygame.transform.scale(load_image('background-field.png'), (880, 880))
    generate_level(load_level('level_1.txt'))

    # Создание спрайтов
    all_sticks = pygame.sprite.Group()
    all_stones = pygame.sprite.Group()
    all_grass = pygame.sprite.Group()
    hero_sprite = pygame.sprite.Group()

    #Стартовые инструменты
    inventory = Inventory()
    arm = Weapon(2, 2)
    inventory.add_thing(arm)
    stick = Weapon(4, 4)
    inventory.add_thing(stick)

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
            elif board.field[x][y] == 'H':
                hero = Hero((x, y))
                board.field[x][y] = hero
                Hero_image(hero, hero_sprite)

    # Непосредственно запуск
    running = True
    while running:
        screen.blit(background, (0, 0))
        board.render()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_a or \
                        event.key == pygame.K_d or event.key == pygame.K_s:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LSHIFT]:
                        hero.rotate(event)
                    else:
                        hero.move(event)

        # Отрисовка объектов
        all_sticks.draw(screen)
        all_stones.draw(screen)
        all_grass.draw(screen)
        hero_sprite.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
