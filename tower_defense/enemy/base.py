import pygame


class Enemy:
    images = []

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_count = 0
        self.health = 0
        self.path = []
        self.speed = 0
        self.should_die = False
        self.image = None

    def draw(self, surf: pygame.Surface):
        self.animation_count += 1
        self.image = self.images[self.animation_count]
        if self.animation_count > len(self.images):
            self.animation_count = 0
        surf.blit(self.image, (self.x, self.y))
        self.move()

    def collide(self, x, y) -> bool:
        if x <= self.x + self.width and x >= self.x:
            if y <= self.y + self.health and y >= self.y:
                return True
        return False

    def move(self):
        pass

    def hit(self) -> bool:
        if self.health == 0:
            self.should_die = True
            return self.should_die
        self.health -= 1
        return self.should_die
