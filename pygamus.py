import pygame as pg
import random, time, sys
from pygame.locals import *

fps = 25
window_w, window_h = 600, 500
block, field_h, field_w = 20, 20, 10

side_freq, down_freq = 0.15, 0.1

side_margin = int((window_w - field_w * block) / 2)
top_margin = window_h - (field_h * block) - 5

colors = ((0, 0, 0), (255, 255, 255))
lightcolors = ((0, 0, 0), (255, 255, 255))

white, gray, black = (255, 255, 255), (185, 185, 185), (0, 0, 0)
brd_color, bg_color, txt_color, title_color, info_color = black, (255, 15, 192), black, (255, 15, 192), black

fig_w, fig_h = 5, 5
empty = 'o'

figures = {'S': [['ooooo',
                  'ooooo',
                  'ooxxo',
                  'oxxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxxo',
                  'oooxo',
                  'ooooo']],
           'Z': [['ooooo',
                  'ooooo',
                  'oxxoo',
                  'ooxxo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'oxxoo',
                  'oxooo',
                  'ooooo']],
           'J': [['ooooo',
                  'oxooo',
                  'oxxxo',
                  'ooooo',
                  'ooooo'],
                 ['ooooo',
                  'ooxxo',
                  'ooxoo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'oxxxo',
                  'oooxo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxoo',
                  'oxxoo',
                  'ooooo']],
           'L': [['ooooo',
                  'oooxo',
                  'oxxxo',
                  'ooooo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxoo',
                  'ooxxo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'oxxxo',
                  'oxooo',
                  'ooooo'],
                 ['ooooo',
                  'oxxoo',
                  'ooxoo',
                  'ooxoo',
                  'ooooo']],
           'I': [['ooxoo',
                  'ooxoo',
                  'ooxoo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'xxxxo',
                  'ooooo',
                  'ooooo']],
           'O': [['ooooo',
                  'ooooo',
                  'oxxoo',
                  'oxxoo',
                  'ooooo']],
           'T': [['ooooo',
                  'ooxoo',
                  'oxxxo',
                  'ooooo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'ooxxo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooooo',
                  'oxxxo',
                  'ooxoo',
                  'ooooo'],
                 ['ooooo',
                  'ooxoo',
                  'oxxoo',
                  'ooxoo',
                  'ooooo']]}


def pauseScreen():
    pause = pg.Surface((600, 500))
    pause.fill((0, 0, 0, 0))
    display_surf.blit(pause, (0, 0))


def main():
    global fps_clock, display_surf, basic_font, big_font
    pg.init()
    fps_clock = pg.time.Clock()
    display_surf = pg.display.set_mode((window_w, window_h))
    basic_font = pg.font.SysFont('arial', 20)
    big_font = pg.font.SysFont('verdana', 45)
    pg.display.set_caption('Тетрис')
    showText('Тетрис')
    image = pg.image.load('tetris.jpg').convert_alpha()
    new_image = pg.transform.scale(image, (300, 500))
    display_surf.blit(new_image, (100, 100))
    while True:
        tetris()
        pauseScreen()
        showText('GAME OVER')


def tetris():
    field = emptyfield()
    last_move_down = time.time()
    last_side_move = time.time()
    last_fall = time.time()
    going_down = False
    going_left = False
    going_right = False
    points = 0
    level, fall_speed = speed(points)
    falling = newfigure()
    nextFig = newfigure()

    while True:
        if falling == None:
            falling = nextFig
            nextFig = newfigure()
            last_fall = time.time()

            if not position(field, falling):
                return
        quitGame()
        for event in pg.event.get():
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    pauseScreen()
                    showText('Пауза')
                    last_fall = time.time()
                    last_move_down = time.time()
                    last_side_move = time.time()
                elif event.key == K_a or event.key == K_LEFT:
                    going_left = False
                elif event.key == K_d or event.key == K_RIGHT:
                    going_right = False
                elif event.key == K_s or event.key == K_DOWN:
                    going_down = False

            elif event.type == KEYDOWN:
                if (event.key == K_a or event.key == K_LEFT) and position(field, falling, adjX=-1):
                    falling['x'] -= 1
                    going_left = True
                    going_right = False
                    last_side_move = time.time()

                elif (event.key == K_d or event.key == K_RIGHT) and position(field, falling, adjX=1):
                    falling['x'] += 1
                    going_right = True
                    going_left = False
                    last_side_move = time.time()

                elif event.key == K_w or event.key == K_UP:
                    falling['rotation'] = (falling['rotation'] + 1) % len(figures[falling['shape']])
                    if not position(field, falling):
                        falling['rotation'] = (falling['rotation'] - 1) % len(figures[falling['shape']])

                elif event.key == K_s or event.key == K_DOWN:
                    going_down = True
                    if position(field, falling, adjY=1):
                        falling['y'] += 1
                    last_move_down = time.time()

                elif event.key == K_RETURN:
                    going_down = False
                    going_left = False
                    going_right = False
                    for i in range(1, field_h):
                        if not position(field, falling, adjY=i):
                            break
                    fallingFig['y'] += i - 1

        if (going_left or going_right) and time.time() - last_side_move > side_freq:
            if going_left and position(field, falling, adjX=-1):
                falling['x'] -= 1
            elif going_right and position(field, falling, adjX=1):
                falling['x'] += 1
            last_side_move = time.time()

        if going_down and time.time() - last_move_down > down_freq and position(field, falling, adjY=1):
            falling['y'] += 1
            last_move_down = time.time()

        if time.time() - last_fall > fall_speed:
            if not position(field, falling, adjY=1):
                addfigure(field, falling)
                points += clearcup(field)
                level, fall_speed = speed(points)
                falling = None
            else:
                falling['y'] += 1
                last_fall = time.time()

        display_surf.fill(bg_color)
        drawTitle()
        gamefield(field)
        drawInfo(points, level)
        if falling != None:
            drawFig(falling)
        pg.display.update()
        fps_clock.tick(fps)


def txtObjects(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def stop():
    pg.quit()
    sys.exit()


def checkKeys():
    quitGame()

    for event in pg.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def showText(text):
    titleSurf, titleRect = txtObjects(text, big_font, title_color)
    titleRect.center = (int(window_w / 2) - 3, int(window_h / 2) - 3)
    display_surf.blit(titleSurf, titleRect)

    pressKeySurf, pressKeyRect = txtObjects('Нажмите SPACE для продолжения', basic_font, title_color)
    pressKeyRect.center = (int(window_w / 2), int(window_h / 2) + 100)
    display_surf.blit(pressKeySurf, pressKeyRect)

    while checkKeys() == None:
        pg.display.update()
        fps_clock.tick()


def quitGame():
    for event in pg.event.get(QUIT):
        stop()
    for event in pg.event.get(KEYUP):
        if event.key == K_ESCAPE:
            stop()
        pg.event.post(event)


def speed(points):
    level = int(points / 10) + 1
    fall_speed = 0.27 - (level * 0.02)
    return level, fall_speed


def newfigure():
    shape = random.choice(list(figures.keys()))
    newFigure = {'shape': shape,
                 'rotation': random.randint(0, len(figures[shape]) - 1),
                 'x': int(field_w / 2) - int(fig_w / 2),
                 'y': -2,
                 'color': random.randint(0, len(colors) - 1)}
    return newFigure


def addfigure(field, fig):
    for x in range(fig_w):
        for y in range(fig_h):
            if figures[fig['shape']][fig['rotation']][y][x] != empty:
                field[x + fig['x']][y + fig['y']] = fig['color']


def emptyfield():
    field = []
    for i in range(field_w):
        field.append([empty] * field_h)
    return field


def infield(x, y):
    return x >= 0 and x < field_w and y < field_h


def position(field, fig, adjX=0, adjY=0):
    for x in range(fig_w):
        for y in range(fig_h):
            abovefield = y + fig['y'] + adjY < 0
            if abovefield or figures[fig['shape']][fig['rotation']][y][x] == empty:
                continue
            if not infield(x + fig['x'] + adjX, y + fig['y'] + adjY):
                return False
            if field[x + fig['x'] + adjX][y + fig['y'] + adjY] != empty:
                return False
    return True


def isCompleted(field, y):
    for x in range(field_w):
        if field[x][y] == empty:
            return False
    return True


def clearcup(field):
    removed_lines = 0
    y = field_h - 1
    while y >= 0:
        if isCompleted(field, y):
            for pushDownY in range(y, 0, -1):
                for x in range(field_w):
                    field[x][pushDownY] = field[x][pushDownY - 1]
            for x in range(field_w):
                field[x][0] = empty
            removed_lines += 1
        else:
            y -= 1
    return removed_lines


def convertCoords(block_x, block_y):
    return (side_margin + (block_x * block)), (top_margin + (block_y * block))


def drawBlock(block_x, block_y, color, pixelx=None, pixely=None):
    if color == empty:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertCoords(block_x, block_y)
    pg.draw.rect(display_surf, colors[color], (pixelx + 1, pixely + 1, block - 1, block - 1), 0, 3)
    pg.draw.rect(display_surf, lightcolors[color], (pixelx + 1, pixely + 1, block - 4, block - 4), 0, 3)
    pg.draw.circle(display_surf, colors[color], (pixelx + block / 2, pixely + block / 2), 5)


def gamefield(field):
    pg.draw.rect(display_surf, brd_color, (side_margin - 4, top_margin - 4, (field_w * block) + 8, (field_h * block) + 8), 5)

    pg.draw.rect(display_surf, bg_color, (side_margin, top_margin, block * field_w, block * field_h))
    for x in range(field_w):
        for y in range(field_h):
            drawBlock(x, y, field[x][y])


def drawTitle():
    titleSurf = big_font.render('Тетрис', True, title_color)
    titleRect = titleSurf.get_rect()
    titleRect.topleft = (window_w - 425, 30)
    display_surf.blit(titleSurf, titleRect)


def drawInfo(points, level):
    pointsSurf = basic_font.render(f'Очки: {points}', True, txt_color)
    pointsRect = pointsSurf.get_rect()
    pointsRect.topleft = (window_w - 550, 180)
    display_surf.blit(pointsSurf, pointsRect)

    levelSurf = basic_font.render(f'Уровень: {level}', True, txt_color)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (window_w - 550, 250)
    display_surf.blit(levelSurf, levelRect)

    pausebSurf = basic_font.render('Пауза: пробел', True, info_color)
    pausebRect = pausebSurf.get_rect()
    pausebRect.topleft = (window_w - 550, 420)
    display_surf.blit(pausebSurf, pausebRect)

    rotationSurf = basic_font.render('Управление: WASD', True, info_color)
    rotationRect = rotationSurf.get_rect()
    rotationRect.topleft = (window_w - 550, 50)
    display_surf.blit(rotationSurf, rotationRect)

    rotSurf = basic_font.render(f'или стрелки', True, info_color)
    rotRect = rotSurf.get_rect()
    rotRect.topleft = (window_w - 390, 50)
    display_surf.blit(rotSurf, rotRect)

    image = pg.image.load('tetris.jpg').convert_alpha()
    new_image = pg.transform.scale(image, (150, 400))
    display_surf.blit(new_image, (430, 100))



def drawFig(fig, pixelx=None, pixely=None):
    figToDraw = figures[fig['shape']][fig['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = convertCoords(fig['x'], fig['y'])

    for x in range(fig_w):
        for y in range(fig_h):
            if figToDraw[y][x] != empty:
                drawBlock(None, None, fig['color'], pixelx + (x * block), pixely + (y * block))


if __name__ == '__main__':
    main()