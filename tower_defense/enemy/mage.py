import pygame

from tower_defense.config import ASSETS_DIR, SPRITE_WIDTH, SPRITE_HEIGHT
from tower_defense.enemy.base import BaseEnemySprite


MAGE_DIR = ASSETS_DIR / 'enemies' / 'mage'


class MageSprite(BaseEnemySprite):
    images = [pygame.transform.scale(pygame.image.load(str(p.absolute())), (SPRITE_WIDTH, SPRITE_HEIGHT))
              for p in MAGE_DIR.glob('*.png')]

    def __init__(self, *groups, surface: pygame.Surface):
        super().__init__(*groups, surface=surface)
        self.velocity = 3
        self.health = 10
