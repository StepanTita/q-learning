import pygame.sprite

from constants import Direction
from field.field import GameField
from sprites.mover import Mover
from sprites.sprite import Spriter


class Enemy(pygame.sprite.Sprite, Spriter, Mover):
    def __init__(self, config, g):
        pygame.sprite.Sprite.__init__(self)
        Spriter.__init__(self, config)
        Mover.__init__(self, config, g)

    def fall(self, g, game_field):
        if Direction.DOWN not in self._cannot_move_dirs(game_field):
            self.is_falling = True
            self.rect.move_ip((0, g))
        else:
            self.is_falling = False

    def get_state(self):
        return self.surf, self.rect, None
