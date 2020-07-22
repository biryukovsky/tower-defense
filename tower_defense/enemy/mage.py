import pygame

from tower_defense.config import ASSETS_DIR, SPRITE_WIDTH, SPRITE_HEIGHT
from tower_defense.path import BOTTOM_OFF_SCREEN, LEFT_TO_BOTTOM


MAGE_DIR = ASSETS_DIR / 'enemies' / 'mage'


class MageSprite(pygame.sprite.Sprite):
    images = [pygame.transform.scale(pygame.image.load(str(p.absolute())), (SPRITE_WIDTH, SPRITE_HEIGHT))
              for p in MAGE_DIR.glob('*.png')]

    def __init__(self, *groups, surface: pygame.Surface):
        super().__init__(*groups)
        self.image = self.images[0]
        self.path = LEFT_TO_BOTTOM
        self.rect = self.image.get_rect(center=self.path[0])

        self.surf = surface
        self.current_path_index = 0
        self.velocity = 3
        self.frame_index = 0
        self.health = 10

    def move(self):
        if self.current_path_index + 1 >= len(self.path):
            point = BOTTOM_OFF_SCREEN
        else:
            point = self.path[self.current_path_index]

        if (self.rect.centerx, self.rect.centery) >= point:
            self.current_path_index += 1

        point_x, point_y = point
        if self.rect.centerx < point_x:
            self.rect.centerx += self.velocity

        if self.rect.centery < point_y:
            self.rect.centery += self.velocity

        if self.current_path_index >= len(self.path):
            self.current_path_index = 0

    def draw(self):
        if self.frame_index >= len(self.images):
            self.frame_index = 0

        self.image = self.images[self.frame_index]
        self.frame_index += 1

        self.surf.blit(self.image, (self.rect.x, self.rect.y))
        self.move()

        if self.should_be_killed():
            self.kill()

    def update(self, *args):
        self.draw()

    def should_be_killed(self):
        conditions = [
            (self.rect.centerx, self.rect.centery) > BOTTOM_OFF_SCREEN,
            self.health == 0,
            self.current_path_index >= len(self.path),
        ]
        return any(conditions)

    def hit(self):
        self.health -= 1
