# Connection to server
LOGIN_URL = 'http://localhost:5000/request/client_endpoint/login'
SAVE_STATS_URL = 'http://localhost:5000/request/client_endpoint/save_stats'

STATS_PATH = "resources/player_info.json"

# Window properties
WIN_WIDTH = 600  # Ширина создаваемого окна
WIN_HEIGHT = 700  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)

# Button properties
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 100
BUTTON_X_COORD = (WIN_WIDTH - BUTTON_WIDTH)//2
BUTTON_FONT_SIZE = 30
BUTTON_SELECT_COLOR = (255, 0, 0)
BUTTON_BASE_COLOR = (255, 165, 0)
BUTTON_FONT = "arial"

# Message properties
MESSAGE_WIDTH = 300
MESSAGE_X_COORD = (WIN_WIDTH - MESSAGE_WIDTH)//2
MESSAGE_FONT_SIZE = 20
MESSAGE_COLOR = (0, 0, 0)
MESSAGE_FONT_COLOR = (255, 255, 255)
MESSAGE_FONT = "verdana"

# Field properties
FIELD_WIDTH = 300
FIELD_X_COORD = (WIN_WIDTH - MESSAGE_WIDTH)//2
FIELD_FONT_SIZE = 15
FIELD_COLOR = (0, 0, 0)
FIELD_FONT_COLOR = (255, 255, 255)
FIELD_FONT = "verdana"

# backgrounds
MAIN_MENU_BACKGROUND = 'image/background/main_menu_bg.jpg'
LEVEL_MENU_BACKGROUND = 'image/background/level_menu_bg.jpg'
EASY_LEVEL_BACKGROUND = 'image/background/easy_level_bg.jpg'
NORMAL_LEVEL_BACKGROUND = 'image/background/normal_level_bg.jpg'
HARD_LEVEL_BACKGROUND = 'image/background/hard_level_bg.jpg'
PLUG_UNDONE_BACKGROUND = 'image/background/plug_undone_bg.jpg'

# running constants
running = True
FRAME_RATE = 60
MainMenuTick = FRAME_RATE
LevelMenuTick = FRAME_RATE
PauseMenuTick = FRAME_RATE
LoginMenuTick = FRAME_RATE
LevelTick = 200
PlugTick = FRAME_RATE


# enemy constants
NORMAL_SPEED = 0.5
FAST_SPEED = NORMAL_SPEED * 3 / 2
MOTHER_SPEED = NORMAL_SPEED * 2 / 3
MINI_SPEED = NORMAL_SPEED * 5 / 4
BOSS_SPEED = NORMAL_SPEED / 3
ENEMY_FONT = "verdana"
ENEMY_FONT_SIZE = 20
ENEMY_TOUCHED_FONT_COLOR = (255, 0, 0)
ENEMY_FONT_COLOR = (255, 255, 255)
ENEMY_COLOR = (255, 255, 0)


# Messages
PLUG_MESSAGE = ["Sorry, this place isn't ready",
                "Go back, please",
                "Level2 and Level3",
                "will be added soon",
                "",
                "Press any key"]

PAUSE_MESSAGE = ["You should return",
                 "They are already",
                 "HERE",
                 "They won't wait",
                 "",
                 "Press any key",
                 "to return to battle"
                 "or Esc button",
                 "to return to level menu"]

LOSE_MESSAGE = ["You died",
                "Monsters killed you",
                "And soon they'll destroy",
                "your home",
                "",
                "Press any key",
                "to try again"]

WIN_MESSAGE = ["You won",
               "Thread has been",
               "contained",
               "But someday they'll",
               "RETURN",
               "",
               "Press any key"]

LEVEL1 = {"commands": [
    {"command": "delay", "time": 1000},
    {"command": "enemy", "type": "normal", "name": "hello"},
    {"command": "delay", "time": 500},
    {"command": "enemy", "type": "normal", "name": "this"},
    {"command": "delay", "time": 500},
    {"command": "enemy", "type": "mini", "name": "is"},
    {"command": "delay", "time": 500},
    {"command": "enemy", "type": "mini", "name": "first"},
    {"command": "delay", "time": 500},
    {"command": "enemy", "type": "normal", "name": "level"}
],
    "background": EASY_LEVEL_BACKGROUND
}

LEVELS = [LEVEL1]
