import copy

import pygame as pg
from utils.assets import AssetManager


class GameSettings:
    DISPLAYSURF = pg.display.set_mode((1010, 730), 0, 32)
    FPS = 50  # кадров в секунду
    fps_eat = 30  # кадров в секунду, еда
    fpsClock = pg.time.Clock()
    # координаты начала,конца и центра
    upx, upy = 20, 20
    dx, dy = 980, 660
    cx, cy = (dx + upx) // 2, (dy + upy) // 2

    # игровое поле - все клетки
    squares_all = {}
    # граф поля - список списков соседей
    game_graph = {}
    # все кнопки
    buttons = []
    for i in range(upx, dx + 1, 40):
        for j in range(upy, dy + 1, 40):
            game_graph.update({(i, j): []})
    for i in game_graph.keys():
        v = list([((i[0] + 40) % (dx + upx), i[1]), ((i[0] - 40) % (dx + upx), i[1]), (i[0], (i[1] + 40) % (dy + upy)),
                  (i[0], (i[1] - 40) % (dy + upy))])
        for k in v:
            game_graph[i].append(k)
    default_graph = copy.deepcopy(game_graph)

    assets = AssetManager()
    assets.load_images()
