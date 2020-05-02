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
MESSAGE_FONT = "verdana"

# backgrounds
MAIN_MENU_BACKGROUND = 'image/background/main_menu_bg.jpg'
LEVEL_MENU_BACKGROUND = 'image/background/level_menu_bg.jpg'
EASY_LEVEL_BACKGROUND = 'image/background/easy_level_bg.jpg'
NORMAL_LEVEL_BACKGROUND = 'image/background/normal_level_bg.jpg'
HARD_LEVEL_BACKGROUND = 'image/background/hard_level_bg.jpg'
PLUG_UNDONE_BACKGROUND = 'image/background/plug_undone_bg.jpg'

# running constants
running = True
MainMenuTick = 50
LevelMenuTick = 50
PauseMenuTick = 50
LevelTick = 200
PlugTick = 50

# Messages
PLUG_MESSAGE = ["Sorry, this place isn't ready",
                "   Go back, please",
                "  Level2 and Level3",
                "  will be added soon",
                "",
                "   Press any key"]

DEATH_MESSAGE = ["  You died",
                 "  Monsters kill you",
                 "And soon they'll destroy",
                 "    your home",
                 "",
                 "   Press any key",
                 "   to try again"]

WIN_MESSAGE = ["   You won",
               "  Thread has been",
               "    contained",
               " But someday they'll",
               "    RETURN",
               "",
               "   Press any key"]

