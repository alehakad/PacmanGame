import os

import pygame as pg


class AssetManager:
    def __init__(self):
        self.images = {}

    def load_images(self):
        # Define the folder containing the images
        base_path = os.path.join(os.path.dirname(__file__), '..', 'images')

        # Load game images
        self.images["p_left"] = pg.image.load(os.path.join(base_path, 'p_left.png'))
        self.images["p_left_eat"] = pg.image.load(os.path.join(base_path, 'p_left_eat.png'))
        self.images["p_right"] = pg.image.load(os.path.join(base_path, 'p_right.png'))
        self.images["p_right_eat"] = pg.image.load(os.path.join(base_path, 'p_right_eat.png'))
        self.images["p_up"] = pg.image.load(os.path.join(base_path, 'p_up.png'))
        self.images["p_up_eat"] = pg.image.load(os.path.join(base_path, 'p_up_eat.png'))
        self.images["p_down"] = pg.image.load(os.path.join(base_path, 'p_down.png'))
        self.images["p_down_eat"] = pg.image.load(os.path.join(base_path, 'p_down_eat.png'))
        self.images["p_stop"] = pg.image.load(os.path.join(base_path, "p_stop.png"))
        self.images["sound_off"] = pg.image.load(os.path.join(base_path, 'sound_off.png'))
        self.images["sound_on"] = pg.image.load(os.path.join(base_path, 'sound_on.png'))
        self.images["gh_b"] = pg.image.load(os.path.join(base_path, 'b_ghost.png'))
        self.images["gh_o"] = pg.image.load(os.path.join(base_path, 'o_ghost.png'))
        self.images["gh_p"] = pg.image.load(os.path.join(base_path, 'p_ghost.png'))
        self.images["gh_r"] = pg.image.load(os.path.join(base_path, 'r_ghost.png'))
        self.images["gh_run_w"] = pg.image.load(os.path.join(base_path, 'running_ghost_w.png'))
        self.images["gh_run_b"] = pg.image.load(os.path.join(base_path, 'running_ghost_b.png'))
        self.images["cherry"] = pg.image.load(os.path.join(base_path, 'cherry.png'))
        self.images["banana"] = pg.image.load(os.path.join(base_path, 'banana.png'))
        self.images["strawberry"] = pg.image.load(os.path.join(base_path, 'strawberry.png'))
        self.images["d_gh"] = pg.image.load(os.path.join(base_path, 'dead_ghost.png'))
        self.images["b_pause"] = pg.image.load(os.path.join(base_path, 'b_pause.png'))
        self.images["b_unpause"] = pg.image.load(os.path.join(base_path, 'b_unpause.png'))
        self.images["home"] = pg.image.load(os.path.join(base_path, 'intro.png'))
        self.images["flag"] = pg.image.load(os.path.join(base_path, 'flag.png'))

        # Load intro images
        self.images["name"] = pg.image.load(os.path.join(base_path, 'name.png'))
        self.images["gh_r_logo"] = pg.image.load(os.path.join(base_path, 'r_ghost_logo.png'))
        self.images["gh_b_logo"] = pg.image.load(os.path.join(base_path, 'b_ghost_logo.png'))
        self.images["gh_o_logo"] = pg.image.load(os.path.join(base_path, 'o_ghost_logo.png'))
        self.images["gh_p_logo"] = pg.image.load(os.path.join(base_path, 'p_ghost_logo.png'))

    def get_image(self, name):
        return self.images.get(name)
