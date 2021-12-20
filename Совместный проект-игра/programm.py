import pygame
import os
import sys

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
    for y in range(len(level)):
        for x in range(len(level[y])):
            board.field[y][x] = level[y][x]


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
    background = pygame.transform.scale(load_image('background-field.png'), (880, 880))
    generate_level(load_level('level_1.txt'))

    # Непосредственно запуск
    running = True
    while running:
        screen.blit(background, (0, 0))
        board.render()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
