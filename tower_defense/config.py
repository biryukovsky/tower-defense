import pathlib

from pygame.constants import USEREVENT


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
FPS = 45

DEFAULT_MONEY = 100

SPRITE_WIDTH = 84
SPRITE_HEIGHT = 64

EVENT_ENEMY_PASSED = USEREVENT + 1
GAME_OVER = USEREVENT + 2

ASSETS_DIR = pathlib.Path('.') / 'tower_defense' / 'assets'

PLAYER_HEALTH = 10
