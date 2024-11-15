import pygame as pg


def init_pygame():
    # main
    pg.init()
    # load images
    pg.display.set_caption('Pac-Man')

    # cursor
    pg.mouse.set_cursor(*pg.cursors.broken_x)
