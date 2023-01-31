import pygame
import sys
import os

WIDTH, HEIGHT = 1000, 700
FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


player = None


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = pos_x, pos_y

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)


def load_level(filename):
    filename = filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры:",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fonred.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 30
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def move(hero, direct, fr=False, fl=False):
    x, y = hero.pos
    print(x, y)
    max_y = len(level_map)
    max_x = len(level_map[0])
    if direct == "up":
        if y > 0 and level_map[y - 1][x] in ".@":
            hero.move(x, y - 1)
    elif direct == "left":
        if x > 0 and level_map[y][x - 1] in ".@":
            hero.move(x - 1, y)
    elif direct == "right":
        if x < max_x - 1 and level_map[y][x + 1] in ".@":
            hero.move(x + 1, y)


pygame.init()
#pygame window
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
pygame.display.set_caption('REDBALL')
clock = pygame.time.Clock()
start_screen()
# возврат из заставки
# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
# задали изображение спрайтов
tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('sky.png')
}
player_image = load_image('red.png')
tile_width = tile_height = 50
level_map = load_level('map.txt')
player, level_x, level_y = generate_level(level_map)
all_sprites.draw(screen)
pygame.display.flip()
# игровой цикл
running = True
flLeft = flRight = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                flLeft = flRight = False
                move(player, "up")
            elif event.key == pygame.K_LEFT:
                flLeft = True
                move(player, "left", flLeft)
            elif event.key == pygame.K_RIGHT:
                flRight = True
                move(player, "right", flRight)
    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    player_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()