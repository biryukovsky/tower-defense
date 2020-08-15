import pygame

from tower_defense.tower.base import (BaseTowerSprite, TOWER_DIR, )
from tower_defense.config import (RED_TOWER_WIDTH, RED_TOWER_HEIGHT, )


class RedTower(BaseTowerSprite):
    def __init__(self, *groups, surface: pygame.SurfaceType, position: tuple):
        self.image = self.load_image()
        self.rect = self.image.get_rect()
        super().__init__(*groups, surface=surface, position=position)

    def load_image(self):
        path = str(TOWER_DIR / 'red_tower.png')
        img = pygame.image.load(path)
        return pygame.transform.scale(img, (RED_TOWER_WIDTH, RED_TOWER_HEIGHT))
