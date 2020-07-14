import pygame

from tower_defense.enemy.base import Enemy
from tower_defense.config import ASSETS_DIR
from tower_defense.path import BOTTOM_OFF_SCREEN


MAGE_DIR = ASSETS_DIR / 'enemies' / 'mage'


class Mage(Enemy):
    images = [pygame.transform.scale(pygame.image.load(str(p.absolute())), (84, 64))
              for p in MAGE_DIR.glob('*.png')]

    def __init__(self, width, height):
        super().__init__(width, height)

    def move(self):
        if self.current_path_index + 1 >= len(self.path):
            point = BOTTOM_OFF_SCREEN
        else:
            point = self.path[self.current_path_index]

        if (self.x, self.y) == point:
            self.current_path_index += 1

        point_x, point_y = point
        if self.x < point_x:
            self.x += 1

        if self.y < point_y:
            self.y += 1

        if self.current_path_index >= len(self.path):
            self.current_path_index = 0
