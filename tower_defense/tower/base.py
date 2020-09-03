import pygame

from tower_defense.config import ASSETS_DIR


__all__ = ['TOWER_DIR', 'BaseTowerSprite', ]


TOWER_DIR = ASSETS_DIR / 'towers'


class BaseTowerSprite(pygame.sprite.Sprite):
    image: pygame.SurfaceType

    def __init__(self, *groups, screen: pygame.SurfaceType, position: tuple,
                 place):
        super().__init__(*groups)

        self.screen = screen
        self.position = position
        self.blit_rect = None
        self.radius_rect = None
        self.radius = 0
        self.place = place
        self.target = None

    def draw_radius(self):
        color = (100, 100, 100, 20)
        pos = self.place.blit_rect.center
        self.radius_rect = pygame.draw.circle(self.screen, color, pos, self.radius, 1)

    def draw(self):
        self.blit_rect = self.screen.blit(self.image, self.position)
        self.draw_radius()

    def set_target(self, enemy):
        if not self.target and enemy.alive():
            self.target = enemy

    def release_target(self):
        if self.target is not None:
            self.target = None

    def update(self, *args):
        self.draw()
