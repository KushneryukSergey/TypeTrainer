from abc import ABC, abstractmethod
from pygame import *
from module.constant import *
from module.action.game_options import *


class Enemy(ABC):
    _font = None
    _color = ENEMY_COLOR

    def __init__(self, name: str, x: int, y=0):
        if not Enemy._font:
            pygame.font.init()
            Enemy._font = pygame.font.SysFont(ENEMY_FONT, ENEMY_FONT_SIZE)
        self._font_color = ENEMY_FONT_COLOR
        self._is_killed = False
        self._prefix = ""
        self._suffix = name
        self._speed = 0
        self._x = x
        self._y = y
        self._height = self._font.size(name)[1] * 5 // 4
        self._width = self._font.size(name+"  ")[0]
        self._render()
        self._prefix_pos = self._prefix_pos = (0, 0)
        self._update_text_pos()

    def update(self, letter=" "):
        self._y = min(self._speed + self._y, WIN_HEIGHT - self._height)
        self._update_text_pos()
        if (not self.is_killed) and letter == self._suffix[0]:
            self._prefix += letter
            self._suffix = self._suffix[1:]
            print("|", self._suffix, "|", sep="")
            if not self._suffix:
                self._is_killed = True
            else:
                self._font_color = ENEMY_TOUCHED_FONT_COLOR
                self._render()
        if self._y + self._height >= WIN_HEIGHT:
            return True
        return False

    @property
    def is_killed(self):
        return self._is_killed

    def _render(self):
        self._prefix_text = self._font.render(self._prefix, 1, ENEMY_COLOR)
        self._suffix_text = self._font.render(self._suffix, 1, self._font_color)

    def _update_text_pos(self):
        self._prefix_pos = (self._x + self._font.size(" ")[0],
                            self._y + (self._height - self._font.size(" ")[1]) / 2)
        self._suffix_pos = (self._x + self._font.size(" "+self._prefix)[0],
                            self._y + (self._height - self._font.size(" ")[1]) / 2)

    def draw(self):
        if not self._is_killed:
            pygame.draw.rect(surface(),
                             self._color,
                             (self._x, self._y, self._width, self._height))
            surface().blit(self._prefix_text, self._prefix_pos)
            surface().blit(self._suffix_text, self._suffix_pos)

    def check_touch(self, letter):
        if self._suffix[0] == letter:
            return True
        return False


class NormalEnemy(Enemy):
    def __init__(self, name: str, x: int, y=0):
        super().__init__(name, x, y)
        self._speed = NORMAL_SPEED


class FastEnemy(Enemy):
    pass


class MotherEnemy(Enemy):
    pass


class MiniEnemy(Enemy):
    def __init__(self, name: str, x: int, y=0):
        super().__init__(name, x, y)
        self._speed = MINI_SPEED


class BossEnemy(Enemy):
    pass
