import pygame

from tower_defense.config import ASSETS_DIR


TOWER_DIR = ASSETS_DIR / 'towers'


class BaseTowerSprite(pygame.sprite.Sprite):
    image: pygame.SurfaceType

    def __init__(self, *groups, surface: pygame.SurfaceType, position: tuple):
        super().__init__(*groups)

        self.surface = surface
        self.position = position
        self.blit_rect = None

    def draw(self):
        self.blit_rect = self.surface.blit(self.image, self.position)

    def update(self, *args):
        self.draw()
