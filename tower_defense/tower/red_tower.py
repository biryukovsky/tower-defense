import pygame

from tower_defense.tower.base import (BaseTowerSprite, TOWER_DIR, )
from tower_defense.config import (RED_TOWER_WIDTH, RED_TOWER_HEIGHT, )


__all__ = ['RedTower', ]


class RedTower(BaseTowerSprite):
    def __init__(self, *groups, screen: pygame.SurfaceType, position: tuple,
                 place):
        self.image = self.load_image()
        self.rect = self.image.get_rect()
        super().__init__(*groups, screen=screen, position=position, place=place)
        self.radius = 145

    def load_image(self):
        path = str(TOWER_DIR / 'red_tower.png')
        img = pygame.image.load(path)
        scaled = pygame.transform.scale(img, (RED_TOWER_WIDTH, RED_TOWER_HEIGHT))
        return scaled.convert_alpha()
