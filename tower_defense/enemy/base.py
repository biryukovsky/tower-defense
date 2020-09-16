from typing import List

import pygame

from tower_defense.path import (LEFT_TO_BOTTOM, BOTTOM_OFF_SCREEN, )
from tower_defense.config import ENEMY_PASSED, ENEMY_MOVE


class BaseEnemySprite(pygame.sprite.Sprite):
    """Base class for enemy sprite

    In the child classes you need to define:
     - `images` as class attribute,
     - inside __init__:
      - `health`
      - `velocity`

    Sprites must be collected in pygame.sprite.Group instance
    for proper deleting them from display
    """

    images: List[pygame.SurfaceType]

    def __init__(self, *groups, screen: pygame.SurfaceType, health: int):
        super().__init__(*groups)
        self.image = self.images[0]
        self.path = LEFT_TO_BOTTOM
        self.rect: pygame.Rect = self.image.get_rect(center=self.path[0])

        self.screen = screen
        self.current_path_index = 0
        self.velocity = 0
        self.frame_index = 0
        self._base_heath = self.health = health

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

        if (self.rect.centerx, self.rect.centery) > BOTTOM_OFF_SCREEN:
            pygame.event.post(pygame.event.Event(ENEMY_PASSED))

        self._push_move_event()

    def _push_move_event(self):
        data = {
            'enemy_obj': self,
        }
        pygame.event.post(pygame.event.Event(ENEMY_MOVE, data))

    def draw_health_bar(self):
        width = self.rect.width
        height = 2
        bg_color = pygame.Color('red')
        fg_color = pygame.Color('green')

        health_width = width / self._base_heath * self.health
        pygame.draw.rect(self.image, bg_color, (0, 0, width, height))
        pygame.draw.rect(self.image, fg_color, (0, 0, health_width, height))

    def draw(self):
        if self.frame_index >= len(self.images):
            self.frame_index = 0

        self.image = self.images[self.frame_index]
        self.frame_index += 1

        self.draw_health_bar()

        # rect.x and rect.y for centering the image
        # in other places we use rect.centerx and rect.centery
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
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
