import pygame

from tower_defense.config import ASSETS_DIR, MAGE_WIDTH, MAGE_HEIGHT
from tower_defense.enemy.base import BaseEnemySprite


MAGE_DIR = ASSETS_DIR / 'enemies' / 'mage'


class MageSprite(BaseEnemySprite):
    images = [pygame.transform.scale(pygame.image.load(str(p)), (MAGE_WIDTH, MAGE_HEIGHT))
              for p in MAGE_DIR.glob('*.png')]

    def __init__(self, *groups, screen: pygame.SurfaceType):
        super().__init__(*groups, screen=screen, health=10)
        self.velocity = 3
