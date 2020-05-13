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
        self._height = MESSAGE_FONT_SIZE * (2 * len(text) + 1)
        if self._height + self._y > WIN_HEIGHT:
            self._y = WIN_HEIGHT - self._height
        self._text_poss = [(self._x + (BUTTON_WIDTH - text_sizes[i][0])//2,
                           self._y + (2*i+1) * MESSAGE_FONT_SIZE)
                           for i in range(len(text_sizes))]

    def draw(self, selected=False):
        pygame.draw.rect(surface(),
                         self._base_color,
                         (self._x, self._y, self._width, self._height))
        for ts, ts_pos in zip(self._text_surfaces, self._text_poss):
            surface().blit(ts, ts_pos)


class Field:
    _font = None

    def __init__(self, x, y, width, base_color=FIELD_COLOR, font_color=FIELD_FONT_COLOR):
        if not Field._font:
            pygame.font.init()
            Field._font = pygame.font.SysFont(FIELD_FONT, FIELD_FONT_SIZE)
        self._x = x
        self._y = y
        self._base_color = base_color
        self._width = width
        self._height = FIELD_FONT_SIZE * 3
        self._text = ""
        self._font_color = font_color
        self._text_surface = None
        self._text_pos = None
        self._update_text()

    def _update_text(self):
        self._text_surface = Field._font.render(self._text, 1, self._font_color)
        self._text_pos = self._text_surface.get_rect(center=(self._x + self._width // 2, self._y + self._height // 2))

    def add_letter(self, letter):
        self._text += letter
        self._update_text()

    def delete_letter(self):
        self._text = self._text[:-1]
        self._update_text()

    @property
    def text(self):
        return self._text

    def draw(self, selected=False):
        pygame.draw.rect(surface(),
                         self._base_color,
                         (self._x, self._y, self._width, self._height))
        surface().blit(self._text_surface, self._text_pos)
