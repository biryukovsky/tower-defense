import pygame

from tower_defense.config import ASSETS_DIR, WINDOW_WIDTH, PLAYER_HEALTH


__all__ = ['HealthBar', ]


HEALTH_BAR_DIR = ASSETS_DIR / 'health_bar'


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, *groups, surface: pygame.Surface, value: int):
        super().__init__(*groups)
        self.width = 350
        self.height = 40
        self.image = self.get_base_img()
        self.rect = self.image.get_rect()

        self.surf = surface
        # TODO: parameterize initial_value
        self.initial_value = PLAYER_HEALTH
        self.value = value

        if self.value > self.initial_value:
            raise ValueError('value cannot be more than '
                             f'initial_value of {self.initial_value}')

    def get_base_img(self):
        path = str((HEALTH_BAR_DIR / 'health_bar_base.png').absolute())
        img_obj = pygame.image.load(path)
        return pygame.transform.scale(img_obj, (self.width, self.height))

    def get_fill_img(self):
        path = str((HEALTH_BAR_DIR / 'health_bar_fill.png').absolute())
        img_obj = pygame.image.load(path)
        return pygame.transform.scale(img_obj, (self.width, self.height))

    @property
    def position(self):
        x = WINDOW_WIDTH // 2 - self.width // 2
        y = 5
        return x, y

    def get_fill_width(self):
        nth = self.width // self.initial_value
        return nth * self.value

    def update(self, *args):
        fill = self.get_fill_img()
        fill_width = self.get_fill_width()
        self.image.blit(fill, (0, 0), (0, 0, fill_width, self.height))

        self.surf.blit(self.image, self.position)
