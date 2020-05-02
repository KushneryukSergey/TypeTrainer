import pygame
from module.constant import DISPLAY


SURFACE = None


def init_game():
    global SURFACE
    pygame.init()
    SURFACE = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("TypeTrainer: kill by words")
    pygame.display.update()


def surface():
    global SURFACE
    return SURFACE
