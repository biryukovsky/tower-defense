import math

import pygame

from tower_defense.config import (WINDOW_HEIGHT, WINDOW_WIDTH, FPS, ASSETS_DIR,
                                  DEFAULT_MONEY, ENEMY_PASSED,
                                  PLAYER_HEALTH, GAME_OVER, ENEMY_MOVE, )
from tower_defense.enemy.mage import MageSprite
from tower_defense.tower.place import TowerPlace
from tower_defense.health_bar import HealthBar
from tower_defense.tower.points import TOWER_PLACE_POINTS
from tower_defense.tower.red_tower import RedTower


class EventHandler:
    _EVENT_TYPE_MAPPING = {
        pygame.QUIT: 'quit',
        pygame.MOUSEBUTTONDOWN: 'mouse_click',
        ENEMY_PASSED: 'deal_damage',
        GAME_OVER: 'game_over',
        ENEMY_MOVE: 'check_radius_collide'
    }

    def __init__(self, game_obj: 'Game', event: pygame.event.EventType):
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
        if btn != pygame.BUTTON_LEFT:
            return
        pos = pygame.mouse.get_pos()
        self._put_tower(pos)

    def check_radius_collide(self):
        # circle collision detection
        # https://www.youtube.com/watch?v=gAkUlyj6irw
        enemy_obj = self.event.dict['enemy_obj']
        enemy_center_x, enemy_center_y = enemy_obj.rect.center
        for tower in self.game.towers:
            circle_center_x, circle_center_y = tower.radius_rect.center
            distance = math.hypot(circle_center_x - enemy_center_x,
                                  circle_center_y - enemy_center_y)
            if distance <= tower.radius:
                is_collide = True
                tower.set_target(enemy_obj)
            else:
                is_collide = False
                tower.release_target()

    def deal_damage(self):
        self.game.health -= 1

    def game_over(self):
        self.quit()

    def _put_tower(self, pos):
        """
        https://stackoverflow.com/questions/44998943/how-to-check-if-the-mouse-is-clicked-in-a-certain-area-pygame
        """
        # check what tower place was clicked
        pl: TowerPlace
        for pl in self.game.tower_places:
            if pl.blit_rect.collidepoint(pos) and pl.is_free:
                # experimentally calculated offset
                tower_pos = (pl.position[0] + 30, pl.position[1] - 60)
                tower = RedTower(screen=self.game.display_surf, position=tower_pos,
                                 place=pl)
                self.game.towers.add(tower)
                # prevent many towers in one place
                pl.is_free = False


class Game:
    def __init__(self):
        self.window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.running = True
        self.display_surf: pygame.SurfaceType = None
        self.clock: pygame.time.Clock = None
        self.enemies = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.tower_places = pygame.sprite.Group()
        self.health = PLAYER_HEALTH
        self.money = DEFAULT_MONEY
        self.bg: pygame.SurfaceType = None
        self.font: pygame.font.Font = None
        self.health_bar: pygame.SurfaceType = None

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

        self.generate_foundations()

    def on_event(self, event: pygame.event.EventType):
        EventHandler(self, event)()

    def cleanup(self):
        pygame.quit()

    def generate_enemies(self):
        mage = MageSprite(screen=self.display_surf)
        self.enemies.add(mage)

    def generate_foundations(self):
        for pos in TOWER_PLACE_POINTS:
            tw = TowerPlace(screen=self.display_surf, position=pos)
            self.tower_places.add(tw)

    def draw(self):
        pygame.time.wait(0)
        fitted_bg = pygame.transform.scale(self.bg, self.window_size)
        self.display_surf.blit(fitted_bg, (0, 0))
        self.draw_health()

        self.enemies.update()
        self.tower_places.update()
        self.towers.update()

        pygame.display.update()
        self.clock.tick(FPS)

    def draw_health(self):
        bar = HealthBar(screen=self.display_surf, value=self.health)
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
