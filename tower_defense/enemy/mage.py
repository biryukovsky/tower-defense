import pygame

from tower_defense.enemy.base import Enemy
from tower_defense.config import ASSETS_DIR


MAGE_DIR = ASSETS_DIR / 'enemies' / 'mage'


class Mage(Enemy):
    images = [pygame.transform.scale(pygame.image.load(str(p.absolute())), (84, 64))
              for p in MAGE_DIR.glob('*.png')]

    # def __init__(self, x, y, width, height):
    #     super().__init__(x, y, width, height)
