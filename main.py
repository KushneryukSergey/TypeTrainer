import pygame
import time
from module.classes.state import *
from module.constant import *
from module.action.game_options import *


def check():
    background = image.load('image/background/main_menu_bg.jpg')
    pygame.display.blit(background, (-400, -150))

    a = []
    while 1:  # Основной цикл программы
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                print(a)
                raise SystemExit("Thank you for playing my game")
            if e.type == pygame.KEYDOWN:
                print(pygame.key.name(e.key))  # return name of key
                if e.key == pygame.K_SPACE:
                    print(" ")
                if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                    pass
                if e.key == pygame.K_BACKSPACE:
                    pass
                if e.key == pygame.K_RETURN:
                    pass
        pygame.display.update()  # обновление и вывод всех изменений на экран


def main():
    init_game()
    game = Game()  # by default game starts in main menu, cut-scene at first play can be added
    while 1:  # main cycle of program
        game.process()


if __name__ == "__main__":
    main()
