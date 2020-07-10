import pathlib

import pygame


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
WINDOW_FLAGS = pygame.HWSURFACE | pygame.DOUBLEBUF
FPS = 30

DEFAULT_MONEY = 100

ASSETS_DIR = pathlib.Path('.') / 'tower_defense' / 'assets'


class Game:
    def __init__(self):
        self._running = True
        self.display_surf: pygame.Surface = None
        self.clock = None
        self.enemies = []
        self.towers = []
        self.health = 10
        self.money = DEFAULT_MONEY
        self.bg: pygame.Surface = None

    def init_game(self):
        pygame.init()
        pygame.display.set_caption('Tower Defense')
        self.clock = pygame.time.Clock()
        self.display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                                                    WINDOW_FLAGS)
        self.bg = pygame.image.load(str(ASSETS_DIR / 'game_bg.png'))

    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self._running = False

    def cleanup(self):
        pygame.quit()

    def draw(self):
        fitted_bg = pygame.transform.scale(self.bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surf.blit(fitted_bg, (0, 0))
        pygame.display.update()
        self.clock.tick(FPS)

    def run(self):
        self.init_game()

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)

            self.draw()

        self.cleanup()


if __name__ == "__main__":
    game = Game()
    game.run()
