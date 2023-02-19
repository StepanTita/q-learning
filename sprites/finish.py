import pygame.sprite

from constants import Color
from sprites.sprite import Spriter


class Finish(pygame.sprite.Sprite, Spriter):
    def __init__(self, config):
        pygame.sprite.Sprite.__init__(self)
        Spriter.__init__(self, config)

        self.surf.fill(Color.GREEN)

    def get_state(self):
        return self.surf, self.rect, None
