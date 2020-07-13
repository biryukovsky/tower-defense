import math

import pygame

from tower_defense.path import (LEFT_TO_BOTTOM, BOTTOM_OFF_SCREEN, )


class Enemy:
    images = []

    def __init__(self, width, height):
        # self.x = x
        # self.y = y
        self.width = width
        self.height = height
        self.animation_count = 0
        self.health = 0
        self.path = LEFT_TO_BOTTOM
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.velocity = 1
        self.should_die = False
        self.image: pygame.Surface = None
        self.current_path_index = 0
        self.move_count = 0
        self.dis = 0

    def draw(self, surf: pygame.Surface):
        # self.animation_count += 1
        # self.image = self.images[self.animation_count]
        if self.image is not None:
            self.image = (pygame.transform.scale(self.image,
                                                 (self.width, self.height))
                          .convert_alpha())

        self.image = self.images[self.animation_count]
        self.animation_count += 1

        if self.animation_count >= len(self.images):
            self.animation_count = 0
        surf.blit(self.image, (self.x, self.y))
        self.move()

    def collide(self, x, y) -> bool:
        if x <= self.x + self.width and x >= self.x:
            if y <= self.y + self.health and y >= self.y:
                return True
        return False

    def move(self):
        x1, y1 = self.path[self.current_path_index]
        if self.current_path_index + 1 >= len(self.path):
            x2, y2 = BOTTOM_OFF_SCREEN
        else:
            x2, y2 = self.path[self.current_path_index + 1]

        move_dis = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        # self.move_count += 1
        # self.move_count += 0.1
        self.move_count += 0.1 * self.velocity
        dirn = x2 - x1, y2 - y1

        move_x, move_y = (self.x + dirn[0] * self.move_count,
                          self.y + dirn[1] * self.move_count)

        self.dis += math.sqrt((move_x - x1) ** 2 + (move_y - y1) ** 2)

        if self.dis >= move_dis:
            self.dis = 0
            self.move_count = 0
            self.current_path_index += 1

            if self.current_path_index >= len(self.path):
                self.current_path_index = 0

        self.x = move_x
        self.y = move_y

    def hit(self) -> bool:
        if self.health == 0:
            self.should_die = True
            return self.should_die
        self.health -= 1
        return self.should_die
