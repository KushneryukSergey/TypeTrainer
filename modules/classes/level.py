from abc import ABC, abstractmethod
from pygame import *


class Level:
    def __init__(self, commands: list, background, constants: dict):
        self._commands = commands
        self._background = background
        self._constants = constants

