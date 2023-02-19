import pygame

from config import read_config
from game.game import Game


def main():
    pygame.init()

    config = read_config('./config.json')
    game = Game('.', config)
    game.run()

    pygame.quit()


if __name__ == '__main__':
    main()
