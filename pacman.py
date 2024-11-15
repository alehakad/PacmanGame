import copy
import math
import random
import sys
import time

import pygame as pg
from pygame.locals import *

from config.init_pygame import init_pygame

init_pygame()

from config.game_state import GameState
from config.settings import GameSettings
from models.board_elements import Button, Square, Text
from models.heros import Ghost, PacMan
from models.menu_elements import MovingEye
from utils import astar
from utils.colors import Colors


def init_heroes():
    GameState.pman = PacMan(GameSettings.upx + 40, GameSettings.upy, 2)

    b_gh = Ghost(GameSettings.cx - 3 * 40, GameSettings.cy + 3 * 40, "b", 3)
    r_gh = Ghost(GameSettings.cx + 3 * 40, GameSettings.cy - 3 * 40, "r", 3)
    p_gh = Ghost(GameSettings.cx + 3 * 40, GameSettings.cy + 3 * 40, "p", 3)
    o_gh = Ghost(GameSettings.cx - 3 * 40, GameSettings.cy - 3 * 40, "o", 3)


def init_field():
    # заполнение поля
    for i in range(GameSettings.upx, GameSettings.dx + 1, 40):
        for j in range(GameSettings.upy, GameSettings.dy + 1, 40):
            Square(i, j)

    GameState.score = Text(15, 'Score: 0', Colors.White.value, Colors.Black.value,
                           GameSettings.upx + 40,
                           GameSettings.dy + 45)

    GameState.bs = Button(950, 710, "sound_off")
    GameState.bp = Button(990, 710, "pause")
    GameState.hm = Button(910, 710, "intro")


def init_music():
    # музыка
    pg.mixer.init()
    pg.mixer.music.load(r'bg_music.mp3')
    pg.mixer.music.play(-1, 0.0)
    pg.mixer.music.pause()


def right_way(side):  # можно ли пойти в данном направлении
    if side == "down":
        test_rect = GameState.pman.image.get_rect(
            center=(GameState.pman.x, GameState.pman.y + GameState.pman.v_stop))
        psq = GameState.pman.get_sq()
        chl = [GameSettings.squares_all[psq]]
        for sq in GameSettings.default_graph[psq]:
            chl.append(GameSettings.squares_all[sq])
        chl.append(GameSettings.squares_all[(psq[0] + 40) % (GameSettings.dx + 40 - GameSettings.upx), (psq[1] + 40) % (
                GameSettings.dy + 40 - GameSettings.upy)])
        chl.append(GameSettings.squares_all[(psq[0] + 40) % (GameSettings.dx + 40 - GameSettings.upx), (psq[1] - 40) % (
                GameSettings.dy + 40 - GameSettings.upy)])
        chl.append(GameSettings.squares_all[(psq[0] - 40) % (GameSettings.dx + 40 - GameSettings.upx), (psq[1] + 40) % (
                GameSettings.dy + 40 - GameSettings.upy)])
        chl.append(GameSettings.squares_all[(psq[0] - 40) % (GameSettings.dx + 40 - GameSettings.upx), (psq[1] - 40) % (
                GameSettings.dy + 40 - GameSettings.upy)])

        for sq in chl:
            for b in sq.borders:
                if test_rect.colliderect(b):
                    return False
        return True
    if side == "up":
        test_rect = GameState.pman.image.get_rect(
            center=(GameState.pman.x, GameState.pman.y - GameState.pman.v_stop))
        psq = GameState.pman.get_sq()
        chl = [GameSettings.squares_all[psq]]
        for sq in GameSettings.default_graph[psq]:
            chl.append(GameSettings.squares_all[sq])
        chl.append(GameSettings.squares_all[(psq[0] + 40) % (GameSettings.dx + 40 - GameSettings.upx), (psq[1] + 40) % (
                GameSettings.dy + 40 - GameSettings.upy)])
        chl.append(GameSettings.squares_all[(psq[0] + 40) % (GameSettings.dx + 40 - GameSettings.upx), (psq[1] - 40) % (
                GameSettings.dy + 40 - GameSettings.upy)])
        chl.append(GameSettings.squares_all[(psq[0] - 40) % (GameSettings.dx + 40 - GameSettings.upx), (psq[1] + 40) % (
                GameSettings.dy + 40 - GameSettings.upy)])
        chl.append(GameSettings.squares_all[(psq[0] - 40) % (GameSettings.dx + 40 - GameSettings.upx), (psq[1] - 40) % (
                GameSettings.dy + 40 - GameSettings.upy)])
        for sq in chl:

            for b in sq.borders:
                if test_rect.colliderect(b):
                    return False
        return True
    if side == "left":
        test_rect = GameState.pman.image.get_rect(
            center=(GameState.pman.x - GameState.pman.v_stop, GameState.pman.y))
        psq = GameState.pman.get_sq()
        chl = [GameSettings.squares_all[psq]]
        for sq in GameSettings.default_graph[psq]:
            chl.append(GameSettings.squares_all[sq])
        chl.append(GameSettings.squares_all[(psq[0] + 40) % (GameSettings.dx + 40 - GameSettings.upx), (psq[1] + 40) % (
                GameSettings.dy + 40 - GameSettings.upy)])
        chl.append(GameSettings.squares_all[(psq[0] + 40) % (GameSettings.dx + 40 - GameSettings.upx), (psq[1] - 40) % (
                GameSettings.dy + 40 - GameSettings.upy)])
        chl.append(GameSettings.squares_all[(psq[0] - 40) % (GameSettings.dx + 40 - GameSettings.upx), (psq[1] + 40) % (
                GameSettings.dy + 40 - GameSettings.upy)])
        chl.append(GameSettings.squares_all[(psq[0] - 40) % (GameSettings.dx + 40 - GameSettings.upx), (psq[1] - 40) % (
                GameSettings.dy + 40 - GameSettings.upy)])

        for sq in chl:

            for b in sq.borders:
                if test_rect.colliderect(b):
                    return False
        return True
    if side == "right":
        test_rect = GameState.pman.image.get_rect(
            center=(GameState.pman.x + GameState.pman.v_stop, GameState.pman.y))
        psq = GameState.pman.get_sq()
        chl = []
        try:
            chl = [GameSettings.squares_all[psq]]
        except:
            print(GameState.pman.x, GameState.pman.y)
        for sq in GameSettings.default_graph[psq]:
            chl.append(GameSettings.squares_all[sq])
        chl.append(GameSettings.squares_all[(psq[0] + 40) % (GameSettings.dx + 40 - GameSettings.upx), (psq[1] + 40) % (
                GameSettings.dy + 40 - GameSettings.upy)])
        chl.append(GameSettings.squares_all[(psq[0] + 40) % (GameSettings.dx + 40 - GameSettings.upx), (psq[1] - 40) % (
                GameSettings.dy + 40 - GameSettings.upy)])
        chl.append(GameSettings.squares_all[(psq[0] - 40) % (GameSettings.dx + 40 - GameSettings.upx), (psq[1] + 40) % (
                GameSettings.dy + 40 - GameSettings.upy)])
        chl.append(GameSettings.squares_all[(psq[0] - 40) % (GameSettings.dx + 40 - GameSettings.upx), (psq[1] - 40) % (
                GameSettings.dy + 40 - GameSettings.upy)])
        for sq in chl:
            for b in sq.borders:
                if test_rect.colliderect(b):
                    return False
        return True


# изменить границы квадрата
def change_borders(x, y, sides, nofood=True, append=False):
    sq1 = GameSettings.squares_all[(x, y)]
    if not append:
        sq1.get_borders(sides)
        sq1.sides = sides
    else:
        sides = list(set(sq1.sides + sides))
        sq1.sides = sides
        sq1.get_borders(sides)

    if nofood:
        sq1.color = Colors.Black.value  # убираем еду
    xsq = x
    ysq = y
    vn = (xsq, ysq)  # текушая вершина
    # изменяем граф
    nv = ((xsq - 40) % (GameSettings.dx + 40 - GameSettings.upx), ysq)
    if "left" in sides:
        if nv in GameSettings.game_graph[vn]:
            GameSettings.game_graph[vn].remove(nv)
            try:
                GameSettings.game_graph[nv].remove(vn)
            except:
                print(nv, vn, 'l')

    elif not append and not (nv in GameSettings.game_graph[vn]):
        GameSettings.game_graph[vn].append(nv)
        GameSettings.game_graph[nv].append(vn)
    nv = ((xsq + 40) % (GameSettings.dx + 40 - GameSettings.upx), ysq)
    if "right" in sides:
        if nv in GameSettings.game_graph[vn]:
            GameSettings.game_graph[vn].remove(nv)
            try:
                GameSettings.game_graph[nv].remove(vn)
            except:
                print(nv, vn, 'r')

    elif not append and not (nv in GameSettings.game_graph[vn]):
        GameSettings.game_graph[vn].append(nv)
        GameSettings.game_graph[nv].append(vn)
    nv = (xsq, (ysq - 40) % (GameSettings.dy + 40 - GameSettings.upy))
    if "up" in sides:
        if nv in GameSettings.game_graph[vn]:
            GameSettings.game_graph[vn].remove(nv)
            try:
                GameSettings.game_graph[nv].remove(vn)
            except:
                print(nv, vn, 'u')

    elif not append and not (nv in GameSettings.game_graph[vn]):
        GameSettings.game_graph[vn].append(nv)
        GameSettings.game_graph[nv].append(vn)
    nv = (xsq, (ysq + 40) % (GameSettings.dy + 40 - GameSettings.upy))
    if "down" in sides:
        if nv in GameSettings.game_graph[vn]:
            GameSettings.game_graph[vn].remove(nv)
            try:
                GameSettings.game_graph[nv].remove(vn)
            except:
                print(nv, vn, 'd')

    elif not append and not (nv in GameSettings.game_graph[vn]):
        GameSettings.game_graph[vn].append(nv)
        GameSettings.game_graph[nv].append(vn)


# нарисовать квадрат по двум крайним точкам
def draw_rect(upx, upy, dx, dy):
    if upx > dx:
        upx, dx = dx, upx
    if upy > dy:
        upy, dy = dy, upy
    if upx == dx and upy == dy:
        change_borders(upx, upy, ["up", "down", "right", "left"])
    elif upx == dx:
        change_borders(upx, upy, ["up", "right", "left"])
        change_borders(upx, dy, ["down", "right", "left"])
        for i in range(upy + 40, dy, 40):
            change_borders(upx, i, ["left", "right"])
    elif upy == dy:
        change_borders(upx, upy, ["down", "up", "left"])
        change_borders(dx, upy, ["down", "up", "right"])
        for i in range(upx + 40, dx, 40):
            change_borders(i, upy, ["up", "down"])

    else:
        change_borders(upx, upy, ["up", "left"])
        change_borders(upx, dy, ["down", "left"])
        change_borders(dx, upy, ["up", "right"])
        change_borders(dx, dy, ["down", "right"])
        for i in range(upx + 40, dx, 40):
            change_borders(i, upy, ["up"])
            change_borders(i, dy, ["down"])
        for i in range(upy + 40, dy, 40):
            change_borders(upx, i, ["left"])
            change_borders(dx, i, ["right"])


def maze(upx, upy, dx, dy, n):  # доделать
    if abs(upx - dx) <= 0 or abs(upy - dy) <= 0:
        return None

    cx = upx + 40 * math.ceil((((dx - upx) / 40) / 2))
    cy = upy + 40 * math.ceil((((dy - upy) / 40) / 2))
    doors = []
    extr1 = False
    extr2 = False
    ch = random.sample([1, 2, 3, 4], 3)
    if 1 in ch:
        doors.append(random.choice([(i, cy) for i in range(upx, cx, 40)]))
    if 2 in ch:
        tmp = random.choice([(i, cy) for i in range(cx, dx + 1, 40)])
        if tmp == (cx, cy):
            extr1 = True
        doors.append(tmp)
    if 3 in ch:
        doors.append(random.choice([(cx, j) for j in range(upy, cy, 40)]))
    if 4 in ch:
        tmp = random.choice([(cx, j) for j in range(cy, dy + 1, 40)])
        if tmp == (cx, cy):
            extr2 = True
        doors.append(tmp)

    for i in range(upx, dx + 1, 40):
        if not ((i, cy) in doors) and i != cx:
            change_borders(i, cy, ["up"], False, True)
    for j in range(upy, dy + 1, 40):
        if not ((cx, j) in doors) and j != cy:
            change_borders(cx, j, ["left"], False, True)
    if (cx, cy) in doors:
        if not (extr1 and extr2):
            if extr1:
                change_borders(cx, cy, ["left"], False, True)
            if extr2:
                change_borders(cx, cy, ["up"], False, True)
    else:
        change_borders(cx, cy, ["left", "up"], False, True)

    maze(upx, upy, cx - 40, cy - 40, n + 1)
    maze(cx, cy, dx, dy, n + 1)
    maze(cx, upy, dx, cy - 40, n + 1)
    maze(upx, cy, cx - 40, dy, n + 1)


# границы - разные для разных уровней
def start_borders(n):  # все обнуляется
    GameSettings.max_score = 0
    GameSettings.game_graph = copy.deepcopy(GameSettings.default_graph)
    for sq in GameSettings.squares_all.values():
        sq.color = Colors.Red.value
        sq.pts = 10
        sq.e = False
        sq.food = pg.Rect(sq.x, sq.y, 5, 5)
        sq.img = False  # бонус
        sq.img_rect = False  # бонус
        sq.sides = []
        sq.borders = []
        sq.get_borders([])
    for gh in GameState.ghosts:
        gh.start_time = time.perf_counter()
        gh.image = gh.default_image
        gh.mode = "chase"
        gh.x, gh.y = gh.startx, gh.starty
        gh.last_sq = GameSettings.game_graph[(gh.x, gh.y)][0]
        gh.i = 0
        gh.ghm = 0
    GameState.pman.lives = 3
    GameState.pman.x, GameState.pman.y = GameState.pman.startx, GameState.pman.starty
    GameState.pman.motion = "STOP"
    GameState.pman.pts = 0
    if n == 1:
        change_borders(GameSettings.upx, GameSettings.upy, ["up", "left"], False)  # 40 по x и y между клетками
        change_borders(GameSettings.dx, GameSettings.dy, ["right", "down"], False)
        change_borders(GameSettings.upx, GameSettings.dy, ["down", "left"], False)
        change_borders(GameSettings.dx, GameSettings.upy, ["up", "right"], False)
        for i in range(1, 24):  # верхняя граница
            if i == 12:
                continue
            change_borders(GameSettings.upx + i * 40, GameSettings.upy, ["up"], False)
        for i in range(1, 24):  # нижняя граница
            if i == 12:
                continue
            change_borders(GameSettings.upx + i * 40, GameSettings.dy, ["down"], False)
        for i in range(2, 15):  # левая граница
            if i % 4:
                change_borders(GameSettings.upx, GameSettings.upy + i * 40, ["left"], False)
        for i in range(2, 15):  # правая граница
            if i % 4:
                change_borders(GameSettings.dx, GameSettings.upy + i * 40, ["right"], False)
        # четверть лабиринта - затем отразить
        for j in [1, -1]:
            if j == 1:
                u = "up"
                d = "down"
            else:
                u = "down"
                d = "up"
            for i in [1, -1]:
                if i == 1:
                    l = "left"
                    r = "right"
                else:
                    r = "left"
                    l = "right"
                draw_rect(GameSettings.cx - i * 12 * 40, GameSettings.cy - j * 8 * 40, GameSettings.cx - i * 12 * 40,
                          GameSettings.cy - j * 8 * 40)
                draw_rect(GameSettings.cx - i * 10 * 40, GameSettings.cy - j * 8 * 40, GameSettings.cx - i * 10 * 40,
                          GameSettings.cy - j * 8 * 40)
                draw_rect(GameSettings.cx - i * 8 * 40, GameSettings.cy - j * 8 * 40, GameSettings.cx - i * 8 * 40,
                          GameSettings.cy - j * 5 * 40)
                draw_rect(GameSettings.cx - i * 40 * 4, GameSettings.cy - j * 8 * 40, GameSettings.cx - i * 40,
                          GameSettings.cy - j * 8 * 40)
                draw_rect(GameSettings.cx - i * 6 * 40, GameSettings.cy - j * 40 * 7, GameSettings.cx - i * 6 * 40,
                          GameSettings.cy - j * 5 * 40)
                draw_rect(GameSettings.cx - i * 6 * 40, GameSettings.cy - j * 6 * 40, GameSettings.cx - i * 4 * 40,
                          GameSettings.cy - j * 6 * 40)
                change_borders(GameSettings.cx - i * 6 * 40, GameSettings.cy - j * 6 * 40, [l])
                draw_rect(GameSettings.cx - i * 12 * 40, GameSettings.cy - j * 6 * 40, GameSettings.cx - i * 10 * 40,
                          GameSettings.cy - j * 5 * 40)
                draw_rect(GameSettings.cx - i * 10 * 40, GameSettings.cy - j * 5 * 40, GameSettings.cx - i * 10 * 40,
                          GameSettings.cy - j * 3 * 40)
                change_borders(GameSettings.cx - i * 10 * 40, GameSettings.cy - j * 5 * 40, [r])
                draw_rect(GameSettings.cx - i * 12 * 40, GameSettings.cy - j * 3 * 40, GameSettings.cx - i * 12 * 40,
                          GameSettings.cy - j * 40)
                draw_rect(GameSettings.cx - i * 12 * 40, GameSettings.cy - j * 40, GameSettings.cx - i * 10 * 40,
                          GameSettings.cy - j * 40)
                change_borders(GameSettings.cx - i * 12 * 40, GameSettings.cy - j * 40, [l, d])
                draw_rect(GameSettings.cx - i * 8 * 40, GameSettings.cy - j * 3 * 40, GameSettings.cx - i * 8 * 40,
                          GameSettings.cy - j * 40)
                draw_rect(GameSettings.cx - i * 8 * 40, GameSettings.cy - j * 40, GameSettings.cx - i * 6 * 40,
                          GameSettings.cy - j * 40)
                change_borders(GameSettings.cx - i * 8 * 40, GameSettings.cy - j * 40, [l, d])
                draw_rect(GameSettings.cx - i * 2 * 40, GameSettings.cy - j * 2 * 40, GameSettings.cx - i * 40,
                          GameSettings.cy - j * 40)
                draw_rect(GameSettings.cx - i * 6 * 40, GameSettings.cy - j * 3 * 40, GameSettings.cx - i * 4 * 40,
                          GameSettings.cy - j * 3 * 40)
                draw_rect(GameSettings.cx - i * 4 * 40, GameSettings.cy - j * 4 * 40, GameSettings.cx - i * 4 * 40,
                          GameSettings.cy - j * 2 * 40)
                draw_rect(GameSettings.cx - i * 4 * 40, GameSettings.cy - j * 4 * 40, GameSettings.cx - i * 40,
                          GameSettings.cy - j * 4 * 40)
                draw_rect(GameSettings.cx - i * 2 * 40, GameSettings.cy - j * 6 * 40, GameSettings.cx - i * 2 * 40,
                          GameSettings.cy - j * 4 * 40)
                change_borders(GameSettings.cx - i * 4 * 40, GameSettings.cy - j * 3 * 40, [r])
                change_borders(GameSettings.cx - i * 4 * 40, GameSettings.cy - j * 4 * 40, [l, u])
                change_borders(GameSettings.cx - i * 2 * 40, GameSettings.cy - j * 4 * 40, [d])
            # центральная линия
            draw_rect(GameSettings.cx, GameSettings.cy - 6 * 40, GameSettings.cx, GameSettings.cy - 6 * 40)
            draw_rect(GameSettings.cx, GameSettings.cy + 6 * 40, GameSettings.cx, GameSettings.cy + 6 * 40)
            draw_rect(GameSettings.cx - 4 * 40, GameSettings.cy, GameSettings.cx - 4 * 40, GameSettings.cy)
            draw_rect(GameSettings.cx + 4 * 40, GameSettings.cy, GameSettings.cx + 4 * 40, GameSettings.cy)
        energy(5)  # энерджайзер - 5 случайных клеток
    else:
        change_borders(GameSettings.upx, GameSettings.upy, ["up", "left"], False)  # 40 по x и y между клетками
        change_borders(GameSettings.dx, GameSettings.dy, ["right", "down"], False)
        change_borders(GameSettings.upx, GameSettings.dy, ["down", "left"], False)
        change_borders(GameSettings.dx, GameSettings.upy, ["up", "right"], False)
        for i in range(1, 24):  # верхняя граница
            change_borders(GameSettings.upx + i * 40, GameSettings.upy, ["up"], False)
        for i in range(1, 24):  # нижняя граница
            change_borders(GameSettings.upx + i * 40, GameSettings.dy, ["down"], False)
        for i in range(1, 16):  # левая граница

            change_borders(GameSettings.upx, GameSettings.upy + i * 40, ["left"], False)
        for i in range(1, 16):  # правая граница
            change_borders(GameSettings.dx, GameSettings.upy + i * 40, ["right"], False)
        maze(GameSettings.upx, GameSettings.upy, GameSettings.dx, GameSettings.dy, 1)  # генерация лабиринта
        energy(15)
        sqr = GameSettings.squares_all[(GameSettings.cx, GameSettings.cy)]
        sqr.img = GameSettings.assets.get_image("flag")
        sqr.img_rect = sqr.img.get_rect(center=(sqr.x, sqr.y))
    for sq in GameSettings.squares_all.values():
        if sq.color != Colors.Black.value:
            GameState.max_score += sq.pts


# прорисовка границ и еды - разная в зависимости от intro
def draw_borders(intro=False):
    if intro:
        for sq in GameSettings.squares_all.values():
            sq.draw_lines()
    else:
        for sq in GameSettings.squares_all.values():
            sq.draw_lines()
            sq.draw_food()


def energy(n):  # энерджайзер
    squares = [sq for sq in GameSettings.squares_all.values() if
               sq.color != Colors.Black.value and sq.img != GameSettings.assets.get_image("flag")]
    for sqr in random.sample(squares, n):
        sqr.food = pg.Rect(sqr.x, sqr.y, 7, 7)
        sqr.pts = 50
        sqr.e = True
        squares.remove(sqr)
    sqr = random.choice(squares)
    sqr.img = random.choice([GameSettings.assets.get_image("cherry"), GameSettings.assets.get_image("strawberry"),
                             GameSettings.assets.get_image("banana")])
    sqr.img_rect = sqr.img.get_rect(center=(sqr.x, sqr.y))
    sqr.pts = 100


# игровое меню
def game_intro():
    init_music()
    init_heroes()
    init_field()

    gen_maze = 1
    intro = True
    # текст
    Text(10, "A.K. 2019 ©", Colors.White.value, Colors.Black.value, GameSettings.dx - 40, GameSettings.dy + 40)
    start = Text(30, "Start Game", Colors.Yellow.value, Colors.Black.value, GameSettings.cx - 4 * 40,
                 GameSettings.upy + 14 * 40)
    e_maze = Text(15, "Easy(classic pacman)", Colors.Yellow.value, Colors.Black.value, GameSettings.cx - 6 * 40,
                  GameSettings.upx + 15 * 40)
    h_maze = Text(15, "Hard(capture the flag)", Colors.Yellow.value, Colors.Black.value, GameSettings.cx - 6 * 40,
                  GameSettings.upx + 16 * 40)
    # глаз за курсором
    r_gh_x, r_gh_y = GameSettings.upx + 18 * 40, GameSettings.dy - 5 * 40
    MovingEye(10, 5, r_gh_x - 9, r_gh_y - 10)
    MovingEye(10, 5, r_gh_x + 9, r_gh_y - 10)

    b_gh_x, b_gh_y = GameSettings.upx + 14 * 40, GameSettings.dy - 5 * 40
    MovingEye(10, 5, b_gh_x - 9, b_gh_y - 10)
    MovingEye(10, 5, b_gh_x + 9, b_gh_y - 10)

    o_gh_x, o_gh_y = GameSettings.upx + 10 * 40, GameSettings.dy - 5 * 40
    MovingEye(10, 5, o_gh_x - 9, o_gh_y - 10)
    MovingEye(10, 5, o_gh_x + 9, o_gh_y - 10)

    p_gh_x, p_gh_y = GameSettings.upx + 6 * 40, GameSettings.dy - 5 * 40
    MovingEye(10, 5, p_gh_x - 9, p_gh_y - 10)
    MovingEye(10, 5, p_gh_x + 9, p_gh_y - 10)

    while intro:
        GameSettings.DISPLAYSURF.fill(Colors.Black.value)
        # текст
        for t in GameState.texts:
            t.draw()

        GameSettings.DISPLAYSURF.blit(GameSettings.assets.get_image("name"),
                                      GameSettings.assets.get_image("name").get_rect(
                                          center=(GameSettings.cx, GameSettings.cy - 3 * 40)))
        # глаз за курсором
        GameSettings.DISPLAYSURF.blit(GameSettings.assets.get_image("gh_r_logo"),
                                      GameSettings.assets.get_image("gh_r_logo").get_rect(center=(r_gh_x, r_gh_y)))
        GameSettings.DISPLAYSURF.blit(GameSettings.assets.get_image("gh_b_logo"),
                                      GameSettings.assets.get_image("gh_b_logo").get_rect(center=(b_gh_x, b_gh_y)))
        GameSettings.DISPLAYSURF.blit(GameSettings.assets.get_image("gh_o_logo"),
                                      GameSettings.assets.get_image("gh_o_logo").get_rect(center=(o_gh_x, o_gh_y)))
        GameSettings.DISPLAYSURF.blit(GameSettings.assets.get_image("gh_p_logo"),
                                      GameSettings.assets.get_image("gh_p_logo").get_rect(center=(p_gh_x, p_gh_y)))

        if gen_maze == 1:
            pg.draw.circle(GameSettings.DISPLAYSURF, Colors.Green.value, (e_maze.textRectObj[0] - 7, e_maze.y), 5)
        elif gen_maze == 2:
            pg.draw.circle(GameSettings.DISPLAYSURF, Colors.Green.value, (h_maze.textRectObj[0] - 7, h_maze.y), 5)
        for e in GameState.eyes:
            e.draw()

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONUP:
                if start.textRectObj.collidepoint(pg.mouse.get_pos()):
                    intro = False
                    GameState.texts.clear()
                    start_borders(gen_maze)

                    Text(15, 'SHADOW', Colors.Red.value, Colors.Black.value, GameSettings.dx - 3 * 40,
                         GameSettings.dy + 45)
                    Text(15, 'SPEEDY', Colors.Pink.value, Colors.Black.value, GameSettings.dx - 6 * 40,
                         GameSettings.dy + 45)
                    Text(15, 'BASHFUL', Colors.Light_Blue.value, Colors.Black.value, GameSettings.dx - 9 * 40,
                         GameSettings.dy + 45)
                    Text(15, 'POKEY', Colors.Orange.value, Colors.Black.value, GameSettings.dx - 12 * 40,
                         GameSettings.dy + 45, )
                    game()
                if e_maze.textRectObj.collidepoint(pg.mouse.get_pos()):
                    gen_maze = 1
                if h_maze.textRectObj.collidepoint(pg.mouse.get_pos()):
                    gen_maze = 2

        pg.display.update()
        GameSettings.fpsClock.tick(GameSettings.FPS)


# запуск игры
def game():
    chase_time = 10
    scatter_time = 5
    frightened_time = 20
    gh_v = 30
    running = True
    while running:
        # очищение экрана
        GameSettings.DISPLAYSURF.fill(Colors.Black.value)

        # вставить текст:
        GameState.score.text = 'Score: ' + str(GameState.pman.pts)
        GameState.score.textSurfaceObj = GameState.score.fontObj.render(GameState.score.text, True, Colors.White.value,
                                                                        Colors.Black.value)
        for t in GameState.texts:
            t.draw()

        # жизни
        for i in range(GameState.pman.lives):
            GameSettings.DISPLAYSURF.blit(GameSettings.assets.get_image("p_right"),
                                          pg.Rect(GameSettings.dx - (20 - i) * 40, GameSettings.dy + 30, 20, 20))

        # кнопка
        for b in GameSettings.buttons:
            b.show()
        # границы
        draw_borders()

        GameState.pman.show()
        for gh in GameState.ghosts:
            gh.show()

            if gh.rect.colliderect(GameState.pman.rect):  # пэкман пойман - reset
                running = False
                if gh.mode != "frightened":
                    GameState.pman.lives -= 1
                    GameState.pman.x = GameState.pman.startx
                    GameState.pman.y = GameState.pman.starty
                    for ghost in GameState.ghosts:
                        ghost.x = ghost.startx
                        ghost.y = ghost.starty
                    GameState.pman.motion = "STOP"
                    if GameState.pman.lives > -1:
                        running = True
                    else:
                        pg.mixer.music.stop()
                        GameState.texts.clear()
                        lose_page(GameState.pman.pts)
                elif gh.image != GameSettings.assets.get_image("d_gh"):
                    GameState.pman.pts += 100
                    running = True
                    gh.image = GameSettings.assets.get_image("d_gh")
                    gh.move = astar.a(gh.get_sq(), (gh.startx, gh.starty), GameSettings.game_graph)
                else:
                    running = True

            if len(GameSettings.game_graph[gh.get_sq()]) != 2 or gh.image == GameSettings.assets.get_image(
                    "d_gh"):  # менять направление только на развилках

                gh.i = 0
                if gh.mode == "chase":
                    gh.move = astar.a(gh.get_sq(), gh.aim(GameState.pman), GameSettings.game_graph)

                    if time.perf_counter() - gh.start_time >= chase_time:
                        gh.mode = "scatter"
                        gh.start_time = time.perf_counter()
                if gh.mode == "scatter":
                    gh.move = astar.a(gh.get_sq(), gh.hide, GameSettings.game_graph)
                    if time.perf_counter() - gh.start_time >= scatter_time:
                        gh.mode = "chase"
                        gh.start_time = time.perf_counter()
                if gh.image == GameSettings.assets.get_image("d_gh"):
                    gh.move = astar.a(gh.get_sq(), (gh.startx, gh.starty), GameSettings.game_graph)
                    if gh.get_sq() == (gh.startx, gh.starty):
                        gh.mode = "chase"
                        gh.image = gh.default_image
                        gh.start_time = time.perf_counter()

                elif gh.mode == "frightened":
                    gh.move = [random.choice(GameSettings.game_graph[gh.get_sq()])]
                    if time.perf_counter() - gh.start_time >= frightened_time:
                        gh.image = gh.default_image
                        gh.mode = "chase"
                        gh.start_time = time.perf_counter()


            else:
                gh.i = 0
                if GameSettings.game_graph[gh.get_sq()][0] != gh.last_sq:
                    gh.move = [GameSettings.game_graph[gh.get_sq()][0]]
                else:
                    gh.move = [GameSettings.game_graph[gh.get_sq()][1]]

            if gh.move != False and gh.i < len(gh.move):
                gh.ghm += 1
                if not (gh.ghm % gh_v):
                    gh.last_sq = gh.get_sq()
                    gh.x = gh.move[gh.i][0]
                    gh.y = gh.move[gh.i][1]
                    gh.i += 1
                    if gh.mode == "frightened" and gh.image != GameSettings.assets.get_image("d_gh"):
                        if gh.image == GameSettings.assets.get_image("gh_run_w"):
                            gh.image = GameSettings.assets.get_image("gh_run_b")
                        else:
                            gh.image = GameSettings.assets.get_image("gh_run_w")
                    gh.ghm = (gh.ghm + 1) % gh_v

        pg.display.update()

        sq = GameSettings.squares_all[GameState.pman.get_sq()]
        if GameState.pman.rect.contains(sq.food):  # если rect_еда внутри rect_pacman
            if sq.color != Colors.Black.value:
                sq.color = Colors.Black.value  # сделать еду невидимой
                GameState.pman.pts += sq.pts  # очки за 1 еду
                if sq.e:
                    for gh in GameState.ghosts:
                        if gh.image != GameSettings.assets.get_image("d_gh"):
                            gh.mode = "frightened"
                            gh.image = GameSettings.assets.get_image("gh_run_w")
                if sq.img == GameSettings.assets.get_image("flag"):
                    running = False
                    GameState.texts.clear()
                    win_page(GameState.pman.pts)
                if sq.img:
                    sq.img = False
            # проверка max_score
            if GameState.pman.pts >= GameState.max_score:
                running = False
                GameState.texts.clear()
                win_page(GameState.pman.pts)
        for event in pg.event.get():

            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONUP:  # нажатие, bs,bp - кнопки

                if GameState.bs.rect.collidepoint(pg.mouse.get_pos()):
                    if GameState.bs.sound:
                        pg.mixer.music.pause()
                        GameState.bs.image = GameSettings.assets.get_image("sound_off")
                        GameState.bs.sound = False
                    else:
                        pg.mixer.music.unpause()
                        GameState.bs.image = GameSettings.assets.get_image("sound_on")
                        GameState.bs.sound = True
                if GameState.bp.rect.collidepoint(pg.mouse.get_pos()):
                    GameState.bp.image = GameSettings.assets.get_image("b_unpause")
                    GameState.bp.show()
                    running = False
                    pause_menu()
                if GameState.hm.rect.collidepoint(pg.mouse.get_pos()):  # доделать
                    running = False
                    GameState.texts.clear()
                    game_intro()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT and right_way("left"):
                    GameState.pman.x -= GameState.pman.v
                    GameState.pman.motion = "LEFT"

                elif event.key == pg.K_RIGHT and right_way("right"):
                    GameState.pman.x += GameState.pman.v
                    GameState.pman.motion = "RIGHT"
                elif event.key == pg.K_UP and right_way("up"):
                    GameState.pman.y -= GameState.pman.v
                    GameState.pman.motion = "UP"
                elif event.key == pg.K_DOWN and right_way("down"):
                    GameState.pman.y += GameState.pman.v
                    GameState.pman.motion = "DOWN"
                elif event.key == pg.K_LSHIFT:  # stop
                    GameState.pman.v = 0
                elif event.key == pg.K_RSHIFT:  # hack
                    GameState.pman.v += 1

        if GameState.pman.motion == "LEFT" and right_way("left"):
            GameState.pman.x -= GameState.pman.v
            if GameState.pman.eat % GameSettings.fps_eat >= GameSettings.fps_eat // 2:
                GameState.pman.image = GameSettings.assets.get_image("p_left")

            else:
                GameState.pman.image = GameSettings.assets.get_image("p_left_eat")

            if GameState.pman.x <= GameSettings.upx - 16:
                GameState.pman.x = GameSettings.dx + 16
            GameState.pman.eat = (GameState.pman.eat + 1) % GameSettings.fps_eat  # чередование картинок
        if GameState.pman.motion == "RIGHT" and right_way("right"):
            GameState.pman.x += GameState.pman.v
            if GameState.pman.eat % GameSettings.fps_eat >= GameSettings.fps_eat // 2:
                GameState.pman.image = GameSettings.assets.get_image("p_right")

            else:
                GameState.pman.image = GameSettings.assets.get_image("p_right_eat")

            if GameState.pman.x >= GameSettings.dx + 16:
                GameState.pman.x = GameSettings.upx - 16
            GameState.pman.eat = (GameState.pman.eat + 1) % GameSettings.fps_eat  # чередование картинок
        if GameState.pman.motion == "UP" and right_way("up"):
            GameState.pman.y -= GameState.pman.v
            if GameState.pman.eat % GameSettings.fps_eat >= GameSettings.fps_eat // 2:
                GameState.pman.image = GameSettings.assets.get_image("p_up")

            else:
                GameState.pman.image = GameSettings.assets.get_image("p_up_eat")

            if GameState.pman.y <= GameSettings.upy - 16:
                GameState.pman.y = GameSettings.dy + 16
            GameState.pman.eat = (GameState.pman.eat + 1) % GameSettings.fps_eat  # чередование картинок
        if GameState.pman.motion == "DOWN" and right_way("down"):
            GameState.pman.y += GameState.pman.v
            if GameState.pman.eat % GameSettings.fps_eat >= GameSettings.fps_eat // 2:
                GameState.pman.image = GameSettings.assets.get_image("p_down")


            else:
                GameState.pman.image = GameSettings.assets.get_image("p_down_eat")

            if GameState.pman.y >= GameSettings.dy + 16:
                GameState.pman.y = GameSettings.upy - 16
            GameState.pman.eat = (GameState.pman.eat + 1) % GameSettings.fps_eat  # чередование картинок

        GameSettings.fpsClock.tick(GameSettings.FPS)


def pause_menu():
    running = True
    while running:
        GameState.bp.show()
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                if GameState.bp.rect.collidepoint(pg.mouse.get_pos()):
                    GameState.bp.image = GameSettings.assets.get_image("b_pause")
                    running = False
                    game()
            if event.type == QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()
        GameSettings.fpsClock.tick(GameSettings.FPS)


def win_page(score):
    GameSettings.DISPLAYSURF.fill(Colors.Black.value)
    running = True
    Text(40, 'YOU WIN', Colors.Red.value, Colors.Black.value, GameSettings.cx, GameSettings.cy)
    Text(20, 'YOUR SCORE: ' + str(score), Colors.Red.value, Colors.Black.value, GameSettings.cx,
         GameSettings.cy + 2 * 40)

    while running:
        GameState.hm.show()
        for t in GameState.texts:
            t.draw()
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                if GameState.hm.rect.collidepoint(pg.mouse.get_pos()):
                    GameState.texts.clear()
                    running = False
                    game_intro()
            if event.type == QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()
        GameSettings.fpsClock.tick(GameSettings.FPS)


def lose_page(score):
    GameSettings.DISPLAYSURF.fill(Colors.Black.value)
    running = True
    Text(40, 'YOU LOSE', Colors.Red.value, Colors.Black.value, GameSettings.cx, GameSettings.cy)
    Text(20, 'YOUR SCORE: ' + str(score), Colors.Red.value, Colors.Black.value, GameSettings.cx,
         GameSettings.cy + 2 * 40)
    while running:
        GameState.hm.show()
        for t in GameState.texts:
            t.draw()
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                if GameState.hm.rect.collidepoint(pg.mouse.get_pos()):
                    GameState.texts.clear()
                    running = False
                    game_intro()
            if event.type == QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()
        GameSettings.fpsClock.tick(GameSettings.FPS)


if __name__ == "__main__":
    game_intro()
