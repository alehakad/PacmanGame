import pygame as pg
from config.game_state import GameState
from config.settings import GameSettings
from utils.colors import Colors


class Square:  # клетки поля - в каждом еда - границы орределяют положение игрока
    def __init__(self, x, y, sides=None, color=Colors.Red.value, b_color=Colors.Blue.value):
        if sides is None:
            sides = []
        self.x = x
        self.y = y
        self.color = color
        self.b_color = b_color  # цвет границы
        self.food = pg.Rect(self.x, self.y, 5, 5)  # еда
        self.pts = 10
        self.e = False  # энерджайзер
        self.img = False  # бонус
        self.img_rect = False  # бонус
        self.centerx = self.food.centerx
        self.centery = self.food.centery
        self.borders = []
        self.get_borders(sides)
        self.sides = sides
        GameSettings.squares_all.update({(self.x, self.y): self})

    def draw_food(self):
        pg.draw.rect(GameSettings.DISPLAYSURF, self.color, self.food)
        if self.img and self.color != Colors.Black.value:
            GameSettings.DISPLAYSURF.blit(self.img, self.img_rect)

    def get_borders(self, sides):
        self.borders = []
        for i in sides:
            if i == "left":
                self.borders.append(pg.Rect(self.centerx - 20, self.centery - 20, 1, 41))
            if i == "right":
                self.borders.append(pg.Rect(self.centerx + 20, self.centery - 20, 1, 41))
            if i == "up":
                self.borders.append(pg.Rect(self.centerx - 20, self.centery - 20, 40, 1))
            if i == "down":
                self.borders.append(pg.Rect(self.centerx - 20, self.centery + 20, 40, 1))

    def draw_lines(self):
        for i in self.borders:
            pg.draw.rect(GameSettings.DISPLAYSURF, self.b_color, i)


# кнопки
class Button():
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        if t == "sound_off":
            self.sound = False
            self.image = GameSettings.assets.get_image("sound_off")
        if t == "pause":
            self.image = GameSettings.assets.get_image("b_pause")
        if t == "intro":
            self.image = GameSettings.assets.get_image("home")

        self.rect = self.image.get_rect(center=(self.x, self.y))
        GameSettings.buttons.append(self)

    def show(self):
        GameSettings.DISPLAYSURF.blit(self.image, self.rect)


# текст
class Text:
    def __init__(self, size, text, fg, bg, x, y):
        self.fontObj = pg.font.SysFont('microsoftsansserif', size)  # change
        self.text = text
        self.x = x
        self.y = y
        self.textSurfaceObj = self.fontObj.render(self.text, True, fg, bg)
        self.textRectObj = self.textSurfaceObj.get_rect()
        self.textRectObj.center = (x, y)
        GameState.texts.append(self)

    def draw(self):
        GameSettings.DISPLAYSURF.blit(self.textSurfaceObj, self.textRectObj)
