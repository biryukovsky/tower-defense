import pygame

from tower_defense.config import (WINDOW_HEIGHT, WINDOW_WIDTH, FPS, ASSETS_DIR,
                                  DEFAULT_MONEY, EVENT_ENEMY_PASSED,
                                  PLAYER_HEALTH, GAME_OVER, )
from tower_defense.enemy.mage import MageSprite
from tower_defense.health_bar import HealthBar


class EventHandler:
    _EVENT_TYPE_MAPPING = {
        pygame.QUIT: 'quit',
        pygame.MOUSEBUTTONDOWN: 'mouse_click',
        EVENT_ENEMY_PASSED: 'deal_damage',
        GAME_OVER: 'game_over',
    }

    def __init__(self, game_obj: 'Game', event: pygame.event.Event):
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
        print(pos)

    def deal_damage(self):
        self.game.health -= 1

    def game_over(self):
        self.quit()


class Game:
    def __init__(self):
        self.window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.running = True
        self.display_surf: pygame.Surface = None
        self.clock: pygame.time.Clock = None
        self.enemies = pygame.sprite.Group()
        self.towers = []
        self.health = PLAYER_HEALTH
        self.money = DEFAULT_MONEY
        self.bg: pygame.Surface = None
        self.font: pygame.font.Font = None
        self.health_bar: pygame.Surface = None

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
        # self.font = pygame.font.SysFont(None, 60)

    def on_event(self, event: pygame.event.Event):
        EventHandler(self, event)()

    def cleanup(self):
        pygame.quit()

    def generate_enemies(self):
        mage = MageSprite(surface=self.display_surf)
        self.enemies.add(mage)

    def draw(self):
        pygame.time.wait(0)
        fitted_bg = pygame.transform.scale(self.bg, self.window_size)
        self.display_surf.blit(fitted_bg, (0, 0))
        self.draw_health()

        for enemy in self.enemies:
            enemy.update()

        pygame.display.update()
        self.clock.tick(FPS)

    def draw_health(self):
        bar = HealthBar(surface=self.display_surf, value=self.health)
        bar.update()

    def run(self):
        self.init_game()
        ticks = pygame.time.get_ticks() + 3 * 1000
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)

            if ticks <= pygame.time.get_ticks():
                ticks = pygame.time.get_ticks() + 3 * 1000
                self.generate_enemies()

            if self.health == 0:
                pygame.event.post(pygame.event.Event(GAME_OVER))

            self.draw()

        self.cleanup()


if __name__ == "__main__":
    game = Game()
    game.run()
