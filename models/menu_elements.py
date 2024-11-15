# глаз
import pygame as pg
from config.game_state import GameState
from config.settings import GameSettings
from utils.colors import Colors


class MovingEye:
    def __init__(self, r1, r2, start_x, start_y):
        self.r1 = r1
        self.r2 = r2
        self.start_x = start_x
        self.start_y = start_y
        GameState.eyes.append(self)

    def draw(self):
        pg.draw.circle(GameSettings.DISPLAYSURF, Colors.White.value, (self.start_x, self.start_y), self.r1)
        r = ((pg.mouse.get_pos()[0] - self.start_x) ** 2 + (pg.mouse.get_pos()[1] - self.start_y) ** 2) ** 0.5
        if r != 0:
            eye_x = int(self.start_x + self.r2 * (pg.mouse.get_pos()[0] - self.start_x) / r)
            eye_y = int(self.start_y + self.r2 * (pg.mouse.get_pos()[1] - self.start_y) / r)
        else:
            eye_x = self.start_x
            eye_y = self.start_y
        pg.draw.circle(GameSettings.DISPLAYSURF, Colors.Black.value, (eye_x, eye_y), self.r2)
