# from __future__ import annotations
from abc import ABC, abstractmethod
from pygame import *


class Game:
    pass


class State(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def run(self):
        return self


class MainMenuState(State):
    def run(self):
        # отрисовка главного меню, возможность выбора кнопок выход, уровни
        pass


class LevelMenuState(State):
    def run(self):
        # отрисовка кнопок выбора первых уровней, кнопки назад
        pass


class LevelState(State):
    def run(self):
        # отрисовка данного уровня, возможность поставить на паузу
        pass


class PauseState(State):
    def __init__(self, state: State):
        super().__init__()
        self._current_level = state

    def run(self):
        # режим паузы с возможностью выйти из уровня или вернуться в игру
        pass


# Это состояние нужно чтобы просто выходить из игры.
# Тогда здесь перед закрытием можно корректно сохранить все необходимое
class ExitState(State):
    def run(self):
        raise SystemExit("Thank you for playing my game!!!")


class Game:
    _state = None

    def __init__(self) -> None:
        pass

    def transition_to(self, state: State):
        self._state = state
        self._state.context = self

    def process(self):
        self._state.run()
