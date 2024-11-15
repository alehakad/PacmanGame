import random

from config.game_state import GameState
from config.settings import GameSettings
from utils import astar


class Hero:
    def __init__(self, x, y, v=0):
        self.rect = None
        self.image = None
        self.x = x
        self.y = y
        self.startx = x
        self.starty = y
        self.v = v
        self.v_stop = v
        self.motion = "STOP"

    def show(self):
        self.rect = self.image.get_rect(center=(self.x, self.y))
        GameSettings.DISPLAYSURF.blit(self.image, self.rect)

    def get_sq(self):  # определение клетки игрока
        xsq = int(round(abs(self.x - GameSettings.upx) / 40) * 40 + GameSettings.upx)
        ysq = int(round(abs(self.y - GameSettings.upy) / 40) * 40 + GameSettings.upy)
        return xsq, ysq


class PacMan(Hero):
    def __init__(self, x, y, v):
        Hero.__init__(self, x, y, v)
        self.image = GameSettings.assets.get_image("p_stop")
        self.lives = 3  # оставшиеся жизни
        self.pts = 0  # набранные очки
        self.eat = 0  # для смены картинок


class Ghost(Hero):
    def __init__(self, x, y, color, v):
        Hero.__init__(self, x, y, v)
        if color == 'b':
            self.image = GameSettings.assets.get_image("gh_b")
            self.default_image = GameSettings.assets.get_image("gh_b")
            self.hide = (GameSettings.dx - 40, GameSettings.dy)  # клетка разбегания
        if color == 'p':
            self.image = GameSettings.assets.get_image("gh_p")
            self.default_image = GameSettings.assets.get_image("gh_p")
            self.hide = (GameSettings.dx - 40, GameSettings.upy)
        if color == 'r':
            self.image = GameSettings.assets.get_image("gh_r")
            self.default_image = GameSettings.assets.get_image("gh_r")
            self.hide = (GameSettings.upx + 40, GameSettings.upy)
        if color == 'o':
            self.image = GameSettings.assets.get_image("gh_o")
            self.default_image = GameSettings.assets.get_image("gh_o")
            self.hide = (GameSettings.upx + 40, GameSettings.dy)
        self.color = color
        # частота смены картинок
        self.i = 0
        self.ghm = 0

        self.mode = "chase"
        self.last_sq = GameSettings.game_graph[(x, y)][0]

        GameState.ghosts.append(self)

    def aim(self, pman):  # целевые клетки приведений
        sq = pman.get_sq()
        col = self.color
        if col == "b":  # для синего цель - конец отрезка между кр. и пк. доработать
            return random.choice(list(GameSettings.squares_all.keys()))
        if col == "p":  # для розового цель - +4 клетки в сторону движения пэкмана
            if pman.motion == "STOP":
                return sq
            if pman.motion == "UP":
                for i in range(3, 0, -1):

                    if (sq[0],
                        (sq[1] - i * 40) % (GameSettings.dy + 40 - GameSettings.upy)) in GameSettings.game_graph.keys():
                        return sq[0], (sq[1] - i * 40) % (GameSettings.dy + 40 - GameSettings.upy)
                return sq
            if pman.motion == "DOWN":
                for i in range(3, 0, -1):

                    if (sq[0],
                        (sq[1] + i * 40) % (GameSettings.dy + 40 - GameSettings.upy)) in GameSettings.game_graph.keys():
                        return sq[0], (sq[1] + i * 40) % (GameSettings.dy + 40 - GameSettings.upy)
                return sq
            if pman.motion == "RIGHT":
                for i in range(3, 0, -1):

                    if ((sq[0] + i * 40) % (GameSettings.dx + 40 - GameSettings.upx),
                        sq[1]) in GameSettings.game_graph.keys():
                        return (sq[0] + i * 40) % (GameSettings.dx + 40 - GameSettings.upx), sq[1]
                return sq
            if pman.motion == "LEFT":
                for i in range(3, 0, -1):

                    if ((sq[0] - i * 40) % (GameSettings.dx + 40 - GameSettings.upx),
                        sq[1]) in GameSettings.game_graph.keys():
                        return (sq[0] - i * 40) % (GameSettings.dx + 40 - GameSettings.upx), sq[1]

                return sq
        if col == "o":  # для орж цель - сам пэкман, если до него меньше 8 клеток(иначе левый нижний угол)
            res = astar.a(sq, self.get_sq(), GameSettings.game_graph)
            if res and len(res) >= 8:
                return sq
            else:
                return GameSettings.upx + 40, GameSettings.dy
        if col == "r":  # для красного цель - сам пэкман
            return sq
