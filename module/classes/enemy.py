from abc import ABC, abstractmethod
from pygame import *


class Enemy(ABC):
    _speed = None
    _name = None
    _x = None
    _y = None

    def move(self):
        pass

    def draw(self):
        pass


class FastEnemy(Enemy):
    def __init__(self, name: str, speed: float):
        self._name = name
        self._speed = speed


class MotherEnemy(Enemy):
    def __init__(self, name: str, speed: float):
        self._name = name
        self._speed = speed


class MiniEnemy(Enemy):
    def __init__(self, name: str, speed: float):
        self._name = name
        self._speed = speed


class BossEnemy(Enemy):
    def __init__(self, name: str, speed: float):
        self._name = name
        self._speed = speed


def draw_enemies(enemies) -> None:
    pass