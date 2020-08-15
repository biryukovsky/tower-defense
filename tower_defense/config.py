import pathlib

from pygame.constants import USEREVENT


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
FPS = 45

DEFAULT_MONEY = 100

MAGE_WIDTH = 84
MAGE_HEIGHT = 64

RED_TOWER_WIDTH = 65
RED_TOWER_HEIGHT = 110

EVENT_ENEMY_PASSED = USEREVENT + 1
GAME_OVER = USEREVENT + 2

ASSETS_DIR = (pathlib.Path('.') / 'tower_defense' / 'assets').absolute()

PLAYER_HEALTH = 10
