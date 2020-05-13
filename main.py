from module.classes.state import Game, LoginMenuState
from module.action.game_options import init_game


def main():
    init_game()
    game = Game(LoginMenuState())  # by default game starts in main menu, cut-scene at first play can be added
    while 1:  # main cycle of program
        game.process()


if __name__ == "__main__":
    main()
