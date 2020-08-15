"""
Расположить основы башен на их местах на основной поверхности
Обрабатывать клик по основе для дальнейшей работы с башнями:
- Поставить башню
- Удалить башню
"""

import pygame

from tower_defense.tower.base import TOWER_DIR


__all__ = ['TowerFoundation', ]


class TowerFoundation(pygame.sprite.Sprite):
    def __init__(self, *groups, surface: pygame.SurfaceType, position: tuple):
        super().__init__(*groups)

        self.size = (124, 66)
        self.image = self.load_image()
        self.rect = self.image.get_rect()

        self.surf = surface
        self.position = position
        self.blit_rect = None

    def load_image(self):
        path = str(TOWER_DIR / 'foundation.png')
        img = pygame.image.load(path)
        return pygame.transform.scale(img, self.size)

    def draw(self):
        self.blit_rect = self.surf.blit(self.image, self.position)

    def update(self, *args):
        self.draw()
