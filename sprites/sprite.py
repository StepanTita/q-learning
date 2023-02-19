import pygame

from constants import Color


class Spriter:
    def __init__(self, config):
        self.surf = pygame.Surface((config.get('width', 50), config.get('height', 50)) )
        self.surf.fill(Color.BLACK)
        self.rect = self.surf.get_rect()
        self.shape = config.get('shape', 'rect')

        self.rect.update(config.get('x', 0), config.get('y', 0), self.surf.get_width(), self.surf.get_height())

    def get_state(self):
        """

        :return:
        Tuple: (surf, pos, direction)
        Where
        surf - is the drawn object Surface object
        pos - position of the object on the screen
        """
        raise Exception('Required method not implemented!')
