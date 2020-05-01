import pygame
from pygame import *
import time
from modules.classes.states import *


WIN_WIDTH = 600  # Ширина создаваемого окна
WIN_HEIGHT = 700  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#004400"
clock = pygame.time.Clock()


def main():
    pygame.init()  # Инициация PyGame, обязательная строчка
    game = Game()
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    # pygame.display.set_caption("image/background/level_menu_bg.jpg")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом
    while 1:  # Основной цикл программы
        background = image.load('image/background/main_menu_bg.jpg')
        screen.blit(background, (-400, -150))
        clock.tick(2)
        pygame.display.update()
        bg = image.load('image/background/level_menu_bg.jpg')
        screen.blit(bg, (-400, -150))
        clock.tick(10)
        pygame.display.update()
        for e in pygame.event.get():  # Обрабатываем события
            print(e.type)
            if e.type == QUIT:
                raise SystemExit("Thank you for playing my game!!!")
                                 # Каждую итерацию необходимо всё перерисовывать
        pygame.display.update()  # обновление и вывод всех изменений на экран


if __name__ == "__main__":
    main()
