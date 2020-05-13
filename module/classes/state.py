from abc import ABC, abstractmethod
import random
import copy
import requests
from module.classes.objects import *
from module.classes.enemy import *
from module.action.game_options import get_level, set_level, surface


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


class LoginMenuState(State, object):
    # отрисовка главного меню, возможность выбора кнопок выход, уровни

    def __init__(self):
        super().__init__()
        self._selections = [2, 4, 5]
        self._selection = 0
        self._objects = []
        self._background = image.load(LEVEL_MENU_BACKGROUND)
        self._objects.append(None)  # для возможных ошибок, связанных с вводом пароля или имени
        self._objects.append(Message(MESSAGE_X_COORD, 250, MESSAGE_WIDTH, ["Enter name:"]))
        self._objects.append(Field(FIELD_X_COORD, 300, FIELD_WIDTH))
        self._objects.append(Message(MESSAGE_X_COORD, 350, MESSAGE_WIDTH, ["Enter password:"]))
        self._objects.append(Field(FIELD_X_COORD, 400, FIELD_WIDTH))
        self._objects.append(Button(BUTTON_X_COORD, 550, BUTTON_WIDTH, BUTTON_HEIGHT,
                                    "Enter", BUTTON_BASE_COLOR, BUTTON_SELECT_COLOR))

    def run(self) -> State:
        self.init_clock(LoginMenuTick)
        self._draw()
        while running:
            for e in pygame.event.get():
                if e.type == QUIT:
                    return ExitState()
                if e.type == pygame.KEYDOWN:
                    if e.key == K_UP:
                        self._selection = (self._selection - 1 + len(self._selections)) % len(self._selections)
                        self._draw()
                    elif e.key == K_DOWN:
                        self._selection = (self._selection + 1) % len(self._selections)
                        self._draw()
                    elif e.key == K_RETURN:
                        if self._selection == 2:
                            answer = self._send_login_request()
                            if answer == "success":
                                return MainMenuState()
                            elif answer == "incorrect":
                                self._objects[0] = Message(MESSAGE_X_COORD, 0, MESSAGE_WIDTH,
                                                           ["Error: incorrect ", "name or password"])
                            else:
                                self._objects[0] = Message(MESSAGE_X_COORD, 0, MESSAGE_WIDTH,
                                                           ["Connection problems",
                                                            "Check your internet",
                                                            "connection"])
                        else:
                            self._selection = (self._selection + 1) % len(self._selections)
                        self._draw()
                    elif e.key == K_BACKSPACE:
                        if self._selection < 2:
                            self._objects[self._selections[self._selection]].delete_letter()
                        self._draw()
                    else:
                        letter = pygame.key.name(e.key)
                        if (letter.isalpha() or letter.isdigit()) and len(letter) == 1 and self._selection < 2:
                            self._objects[self._selections[self._selection]].add_letter(letter)
                        self._draw()

    def _send_login_request(self):
        request_to_send = {"name": self._objects[self._selections[0]].text,
                           "pass": self._objects[self._selections[1]].text}
        try:
            result = requests.post(LOGIN_URL, json=request_to_send)
        except requests.exceptions.ConnectionError as e:
            return False
        else:
            return result.json()["status"]

    def _draw(self):
        surface().blit(self._background, (0, 0))
        for i in range(len(self._objects)):
            if self._objects[i] is not None:
                self._objects[i].draw(self._selections[self._selection] == i)
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
                        if self._selection < len(LEVELS):
                            set_level(LEVELS[self._selection])
                            return LevelState()
                        else:
                            return PlugState()

    def _draw(self):
        surface().blit(self._background, (0, 0))
        for i in range(len(self._buttons)):
            self._buttons[i].draw(self._selection == i)
        pygame.display.update()


class LevelState(State):
    _commands = []
    _command_index = 0
    _target = None
    _win_status = False
    _lose_status = False
    _win_message: Message = None
    _lose_message: Message = None
    _last_moment: int = None
    _clock: pygame.time.Clock() = None

    def __init__(self):
        super().__init__()
        self._last_moment = pygame.time.get_ticks()
        self._build_level(get_level())

    def _build_level(self, level):
        if not self._commands:
            self._last_moment = pygame.time.get_ticks()
            self._clock = pygame.time.Clock()
            self._background = image.load(level["background"])
            self._commands = copy.deepcopy(level["commands"])
            self._command_index = 0
            self._enemies = []

    def _clear_level(self):
        self._background = ""
        self._commands = None
        self._target = None
        self._win_status = False
        self._lose_status = False
        self._enemies = []

    def run(self) -> State:
        self.init_clock(LevelTick)
        a = 0
        while running:
            self._draw()
            if self._command_index < len(self._commands):
                if self._commands[self._command_index]["command"] == "delay":
                    new_moment = pygame.time.get_ticks()
                    if self._commands[self._command_index]["time"] <= new_moment - self._last_moment:
                        self._command_index += 1
                    else:
                        self._commands[self._command_index]["time"] -= new_moment - self._last_moment
                    self._last_moment = new_moment
                elif self._commands[self._command_index]["command"] == "enemy":
                    self._add_enemy(self._commands[self._command_index]["type"],
                                    self._commands[self._command_index]["name"],
                                    random.randint(100, 550), 0)
                    self._command_index += 1

            for e in pygame.event.get():
                if e.type == QUIT:
                    self._clear_level()
                    return ExitState()
                elif (self._win_status or self._lose_status) and e.type == pygame.KEYDOWN:
                    self._clear_level()
                    return LevelMenuState()
                elif e.type == pygame.KEYDOWN:
                    if e.key == K_ESCAPE:
                        return PauseMenuState()
                    letter = pygame.key.name(e.key)
                    if self._target is None:
                        for enemy in self._enemies:
                            if enemy.check_touch(letter):
                                self._target = enemy
                                break
                    if self._target is not None:
                        self._target.update(letter)
                        self._target.update(" ")
                        if self._target.is_killed:
                            self._enemies.remove(self._target)
                            self._target = None
            self._draw()
            self._clock.tick()

    def _draw(self):
        self._update()
        surface().blit(self._background, (0, 0))
        for enemy in self._enemies:
            if self._target is not enemy:
                enemy.draw()
        if self._target is not None:
            self._target.draw()
        if self._win_status:
            self._win_message.draw()
        if self._lose_status:
            self._lose_message.draw()
        pygame.display.update()

    def _check_status(self):
        if self._win_status:
            if self._win_message is None:
                self._win_message = Message(MESSAGE_X_COORD, 200, MESSAGE_WIDTH, WIN_MESSAGE, (255, 165, 0))
        if self._lose_status:
            if self._lose_message is None:
                self._lose_message = Message(MESSAGE_X_COORD, 200, MESSAGE_WIDTH, LOSE_MESSAGE, (0, 0, 0))

    def _update(self):
        self._lose_status = any(enemy.update() for enemy in self._enemies)
        self._win_status = not len(self._enemies) and self._command_index == len(self._commands)
        self._check_status()

    def _add_enemy(self, enemy, name, x_pos, y_pos):
        if enemy == "normal":
            self._enemies.append(NormalEnemy(name, x_pos, y_pos))
        if enemy == "mini":
            self._enemies.append(MiniEnemy(name, x_pos, y_pos))

    def return_to_menu(self):
        self._clear_level()


class PauseMenuState(State):
    def __init__(self):
        super().__init__()
        self._messages = []
        self._background = image.load(PLUG_UNDONE_BACKGROUND)
        self._messages.append(Message(MESSAGE_X_COORD, 400, MESSAGE_WIDTH, PAUSE_MESSAGE))

    def run(self) -> State:
        self.init_clock(PauseMenuTick)
        self._draw()
        while running:
            for e in pygame.event.get():
                if e.type == QUIT:
                    return ExitState()
                if e.type == pygame.KEYDOWN:
                    if e.key == K_ESCAPE:
                        LevelState().return_to_menu()
                        return LevelMenuState()
                    return LevelState()

    def _draw(self):
        surface().blit(self._background, (0, 0))
        for i in range(len(self._messages)):
            self._messages[i].draw()
        pygame.display.update()


class PlugState(State):
    # отрисовка кнопок выбора первых уровней, кнопки назад

    def __init__(self):
        super().__init__()
        self._messages = []
        self._background = image.load(PLUG_UNDONE_BACKGROUND)
        self._messages.append(Message(MESSAGE_X_COORD, 400, MESSAGE_WIDTH,
                                      PLUG_MESSAGE, MESSAGE_COLOR))

    def run(self) -> State:
        self.init_clock(PlugTick)
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
            self._messages[i].draw()
        pygame.display.update()


# Это состояние нужно чтобы просто выходить из игры.
# Тогда здесь перед закрытием можно корректно сохранить
# все необходимое (статистику, прошел ли игрок обучение и тп)
class ExitState(State):
    def run(self):
        pygame.display.quit()
        pygame.quit()
        raise SystemExit("Thank you for playing my game!!!")


class Game:
    def __init__(self, state=MainMenuState()):
        self._state = state

    def _transition_to(self, state: State):
        self._state = state

    def process(self):
        self._transition_to(self._state.run())


if __name__ == "__main__":
    pass
