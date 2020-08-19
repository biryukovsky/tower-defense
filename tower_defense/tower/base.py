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

    def draw_radius(self):
        color = (100, 100, 100, 20)
        pos = self.place.blit_rect.center
        rad_surf = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA, 32)
        self.radius_rect = pygame.draw.circle(rad_surf, color, (0, 0), self.radius, 1)
        self.screen.blit(rad_surf, pos)
        # self.radius_rect = pygame.draw.circle(self.screen, color, pos, self.radius, 1)

    def draw(self):
        self.blit_rect = self.screen.blit(self.image, self.position)
        self.draw_radius()

    def update(self, *args):
        self.draw()
