from pygame import *
from module.constant import *
from module.action.game_options import surface
import pygame


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


class Message:
    _font = None

    def __init__(self, x, y, width, text, base_color=MESSAGE_COLOR, font_color=MESSAGE_FONT_COLOR):
        if not Message._font:
            pygame.font.init()
            Message._font = pygame.font.SysFont(MESSAGE_FONT, MESSAGE_FONT_SIZE)
        self._x = x
        self._y = y
        self._base_color = base_color
        self._width = width
        self._text = text
        self._text_surfaces = [Message._font.render(line, 1, font_color) for line in self._text]
        text_sizes = [Message._font.size(line) for line in self._text]
        self._text_poss = [(self._x + (BUTTON_WIDTH - text_sizes[i][0])//2,
                           self._y + (2*i+1) * MESSAGE_FONT_SIZE)
                           for i in range(len(text_sizes))]
        self._height = MESSAGE_FONT_SIZE * (2*len(text)+1)

    def draw(self):
        pygame.draw.rect(surface(),
                         self._base_color,
                         (self._x, self._y, self._width, self._height))
        for ts, ts_pos in zip(self._text_surfaces, self._text_poss):
            surface().blit(ts, ts_pos)
