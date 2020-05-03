import pygame
from module.constant import DISPLAY
import random


SURFACE = None
LEVEL = None


def init_game():
    global SURFACE
    pygame.init()
    random.seed()
    SURFACE = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("TypeTrainer: kill by words")
    pygame.display.update()


def surface():
    global SURFACE
    return SURFACE


def set_level(level):
    global LEVEL
    LEVEL = level


def get_level():
    global LEVEL
    return LEVEL
