from abc import ABC, abstractmethod
from pygame import *


class Command(ABC):
    def __init__(self, keyword):
        self._keyword = keyword

    @property
    def keyword(self):
        return self._keyword
