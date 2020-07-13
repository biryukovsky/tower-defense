import pygame

from tower_defense.config import (WINDOW_HEIGHT, WINDOW_WIDTH, FPS, ASSETS_DIR,
                                  DEFAULT_MONEY, )
# from tower_defense.enemy.mage import Mage


class EventHandler:
    _EVENT_TYPE_MAPPING = {
        pygame.QUIT: 'quit',
        pygame.MOUSEBUTTONDOWN: 'mouse_click',
    }

    def __init__(self, game_obj, event: pygame.event.Event):
        self.game = game_obj
        self.event = event

    def __call__(self, *args, **kwargs):
        return self.handle()

    def handle(self):
        try:
            method_name = self._EVENT_TYPE_MAPPING.get(self.event.type)
            return getattr(self, method_name)()
        except (TypeError, AttributeError):
            return

    def quit(self):
        self.game.running = False

    def mouse_click(self):
        btn = self.event.button
        if not btn == pygame.BUTTON_LEFT:
            return
        pos = pygame.mouse.get_pos()


class Game:
    def __init__(self):
        self.window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.running = True
        self.display_surf: pygame.Surface = None
        self.clock: pygame.time.Clock = None
        self.enemies = [
            # Mage(75, 63),
        ]
        self.towers = []
        self.health = 10
        self.money = DEFAULT_MONEY
        self.bg: pygame.Surface = None

    def init_game(self):
        # ATTENTION! High CPU load
        # Should try 2.0.0dev or build 1.9.6 from source
        # pygame.init()
        pygame.display.init()
        pygame.font.init()
        pygame.display.set_caption('Tower Defense')
        self.clock = pygame.time.Clock()
        self.display_surf = pygame.display.set_mode(self.window_size)
        self.bg = pygame.image.load(str(ASSETS_DIR / 'game_bg.png'))

    def on_event(self, event: pygame.event.Event):
        EventHandler(self, event)()

    def cleanup(self):
        pygame.quit()

    def draw(self):
        pygame.time.wait(0)
        fitted_bg = pygame.transform.scale(self.bg, self.window_size)
        self.display_surf.blit(fitted_bg, (0, 0))

        for enemy in self.enemies:
            enemy.draw(self.display_surf)

        pygame.display.update()
        self.clock.tick(FPS)

    def run(self):
        self.init_game()

        while self.running:
            for event in pygame.event.get():
                self.on_event(event)

            enemies_to_delete = []
            for enemy in self.enemies:
                if (enemy.x, enemy.y) > self.window_size:
                    enemies_to_delete.append(enemy)

            for e in enemies_to_delete[:]:
                self.enemies.remove(e)
                del e

            self.draw()

        self.cleanup()


if __name__ == "__main__":
    game = Game()
    game.run()
