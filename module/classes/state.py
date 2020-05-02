from abc import ABC, abstractmethod
from typing import Optional
import pygame
from pygame import *
from module.constant import *
from module.action.game_options import surface


class Game:
    pass


class State(ABC):
    def __init__(self):
        self._clock = None

    @abstractmethod
    def run(self):
        return self

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(State, cls).__new__(cls)
        return cls.instance

    def init_clock(self, state_tick):
        if self._clock is None:
            self._clock = time.Clock()
        self._clock.tick_busy_loop(state_tick)


class Button:
    _font = None

    def __init__(self, x, y, width, height, text, base_color, select_color):
        if not Button._font:
            pygame.font.init()
            Button._font = pygame.font.SysFont(BUTTON_FONT, BUTTON_FONT_SIZE)
        self._x = x
        self._y = y
        self._base_color = base_color
        self._select_color = select_color
        self._width = width
        self._height = height
        self._text = text
        self._text_surface = Button._font.render(self._text, 1, (0, 0, 0))
        text_sizes = Button._font.size(self._text)
        self._text_pos = (self._x + (BUTTON_WIDTH - text_sizes[0])//2,
                          self._y + (BUTTON_HEIGHT - text_sizes[1])//2)

    def draw(self, selected):
        pygame.draw.rect(surface(),
                         self._select_color if selected else self._base_color,
                         (self._x, self._y, self._width, self._height))
        surface().blit(self._text_surface, self._text_pos)


class MainMenuState(State, object):
    # отрисовка главного меню, возможность выбора кнопок выход, уровни

    def __init__(self):
        super().__init__()
        self._selection = 0
        self._buttons = []
        self._background = image.load(MAIN_MENU_BACKGROUND)
        self._buttons.append(Button(BUTTON_X_COORD, 200, BUTTON_WIDTH, BUTTON_HEIGHT,
                                    "LEVELS", BUTTON_BASE_COLOR, BUTTON_SELECT_COLOR))
        self._buttons.append(Button(BUTTON_X_COORD, 400, BUTTON_WIDTH, BUTTON_HEIGHT,
                                    "EXIT", BUTTON_BASE_COLOR, BUTTON_SELECT_COLOR))

    def run(self) -> State:
        self.init_clock(MainMenuTick)
        self._draw()
        while running:
            for e in pygame.event.get():
                if e.type == QUIT:
                    return ExitState()
                if e.type == pygame.KEYDOWN:
                    if e.key == K_UP:
                        self._selection = (self._selection - 1 + len(self._buttons)) % len(self._buttons)
                        self._draw()
                    if e.key == K_DOWN:
                        self._selection = (self._selection + 1) % len(self._buttons)
                        self._draw()
                    if e.key == K_RETURN:
                        if self._selection:
                            return ExitState()
                        else:
                            return LevelMenuState()

    def _draw(self):
        surface().blit(self._background, (0, 0))
        for i in range(len(self._buttons)):
            self._buttons[i].draw(self._selection == i)
        pygame.display.update()


class LevelMenuState(State):
    # отрисовка кнопок выбора первых уровней, кнопки назад

    def __init__(self):
        super().__init__()
        self._selection = 0
        self._buttons = []
        self._background = image.load(LEVEL_MENU_BACKGROUND)
        self._buttons.append(Button(BUTTON_X_COORD, 100, BUTTON_WIDTH, BUTTON_HEIGHT,
                                    "LEVEL1", BUTTON_BASE_COLOR, BUTTON_SELECT_COLOR))
        self._buttons.append(Button(BUTTON_X_COORD, 300, BUTTON_WIDTH, BUTTON_HEIGHT,
                                    "LEVEL2", BUTTON_BASE_COLOR, BUTTON_SELECT_COLOR))
        self._buttons.append(Button(BUTTON_X_COORD, 500, BUTTON_WIDTH, BUTTON_HEIGHT,
                                    "LEVEL3", BUTTON_BASE_COLOR, BUTTON_SELECT_COLOR))

    def run(self) -> State:
        self.init_clock(LevelMenuTick)
        self._draw()
        while running:
            for e in pygame.event.get():
                if e.type == QUIT:
                    return ExitState()
                if e.type == pygame.KEYDOWN:
                    if e.key == K_ESCAPE:
                        return MainMenuState()
                    if e.key == K_UP:
                        self._selection = (self._selection - 1 + len(self._buttons)) % len(self._buttons)
                        self._draw()
                    if e.key == K_DOWN:
                        self._selection = (self._selection + 1) % len(self._buttons)
                        self._draw()
                    if e.key == K_RETURN:
                        if self._selection == 0:
                            return LevelMenuState()
                        else:
                            return PlugState()

    def _draw(self):
        surface().blit(self._background, (0, 0))
        for i in range(len(self._buttons)):
            self._buttons[i].draw(self._selection == i)
        pygame.display.update()


class LevelState(State):
    def run(self):
        # отрисовка данного уровня, возможность поставить на паузу
        return self


class PauseMenuState(State):
    def run(self):
        # режим паузы с возможностью выйти из уровня или вернуться в игру
        return MainMenuState()


class Message:
    _font = None

    def __init__(self, x, y, width, text, base_color):
        if not Message._font:
            pygame.font.init()
            Message._font = pygame.font.SysFont(MESSAGE_FONT, MESSAGE_FONT_SIZE)
        self._x = x
        self._y = y
        self._base_color = base_color
        self._width = width
        self._text = text
        self._text_surfaces = [Message._font.render(line, 1, (255, 255, 255)) for line in self._text]
        text_sizes = [Message._font.size(line) for line in self._text]
        self._text_poss = [(self._x + (BUTTON_WIDTH - text_sizes[i][0])//2,
                           self._y + (2*i+1) * MESSAGE_FONT_SIZE)
                           for i in range(len(text_sizes))]
        self._height = MESSAGE_FONT_SIZE * (2*len(text)+1)

    def draw(self, selected):
        pygame.draw.rect(surface(),
                         self._base_color,
                         (self._x, self._y, self._width, self._height))
        for ts, ts_pos in zip(self._text_surfaces, self._text_poss):
            surface().blit(ts, ts_pos)


class PlugState(State):
    # отрисовка кнопок выбора первых уровней, кнопки назад

    def __init__(self):
        super().__init__()
        self._selection = 0
        self._messages = []
        self._background = image.load(PLUG_UNDONE_BACKGROUND)
        self._messages.append(Message(MESSAGE_X_COORD, 400, MESSAGE_WIDTH,
                              PLUG_MESSAGE, MESSAGE_COLOR))

    def run(self) -> State:
        self.init_clock(LevelMenuTick)
        self._draw()
        while running:
            for e in pygame.event.get():
                if e.type == QUIT:
                    return ExitState()
                if e.type == pygame.KEYDOWN:
                    return LevelMenuState()

    def _draw(self):
        surface().blit(self._background, (0, 0))
        for i in range(len(self._messages)):
            self._messages[i].draw(self._selection == i)
        pygame.display.update()


# Это состояние нужно чтобы просто выходить из игры.
# Тогда здесь перед закрытием можно корректно сохранить все необходимое
class ExitState(State):
    def run(self):
        raise SystemExit("Thank you for playing my game!!!")


class Game:
    def __init__(self, state=MainMenuState()):
        self._state = state

    def transition_to(self, state: State):
        self._state = state

    def process(self):
        self.transition_to(self._state.run())


if __name__ == "__main__":
    pass


