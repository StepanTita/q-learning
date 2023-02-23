from collections import namedtuple

import pygame

from constants import Direction
from sprites.mover import Mover
from sprites.sprite import Spriter

Circle = namedtuple("Circle", "pos radius")


def inverse_dir(move_dir):
    if move_dir == Direction.LEFT:
        return Direction.RIGHT
    elif move_dir == Direction.RIGHT:
        return Direction.LEFT
    elif move_dir == Direction.UP:
        return Direction.DOWN
    elif move_dir == Direction.DOWN:
        return Direction.UP


class Player(pygame.sprite.Sprite, Spriter, Mover):
    def __init__(self, config, g):
        pygame.sprite.Sprite.__init__(self)
        Spriter.__init__(self, config)
        Mover.__init__(self, config, g)

        self.is_jumping = False

        self.jump_height = config['jump_height']
        self.yv = self.jump_height

    def _move_dirs(self, x, y):
        dirs_list = []
        if x > 0:
            dirs_list.append(Direction.RIGHT)
        elif x < 0:
            dirs_list.append(Direction.LEFT)

        if y < 0:
            dirs_list.append(Direction.UP)
        elif y > 0:
            dirs_list.append(Direction.DOWN)

        if len(dirs_list) == 0:
            dirs_list.append(Direction.STAY)
        return dirs_list

    def jump(self, game_field):
        if not self.is_falling and not self.is_jumping:
            self.is_jumping = True
            self.step *= 2
        if self.is_jumping:
            self.yv -= self.g * self.weight
            if self.yv > -self.jump_height:
                self.move(self._move_dirs(0, -self.yv)[0], game_field, by=-self.yv)
            else:
                self._end_jump()
            return

    def _end_jump(self):
        self.yv = self.jump_height
        self.is_jumping = False
        self.step /= 2

    def fall(self, g, game_field):
        if Direction.DOWN not in self._cannot_move_dirs(game_field):
            self.is_falling = True
            self.rect.move_ip((0, g))
        else:
            self.is_falling = False

    def get_state(self):
        return self.surf, self.rect, Direction.UP if self.is_jumping else self.last_dir
