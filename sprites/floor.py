import pygame.sprite

from sprites.sprite import Spriter


class Floor(pygame.sprite.Sprite, Spriter):
    def __init__(self, config):
        pygame.sprite.Sprite.__init__(self)
        Spriter.__init__(self, config)

    def get_state(self):
        return self.surf, self.rect, None
