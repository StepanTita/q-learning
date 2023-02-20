from collections import namedtuple

import pygame

from constants import Direction
from field.field import GameField
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


class Player(pygame.sprite.Sprite, Spriter):
    def __init__(self, config, g):
        pygame.sprite.Sprite.__init__(self)
        Spriter.__init__(self, config)

        self.is_jumping = False
        self.is_falling = False

        self.step = config['step']
        self.weight = config['weight']
        self.g = g

        self.jump_height = config['jump_height']
        self.yv = self.jump_height

        self.last_dir = None

    def move(self, move_dir: Direction, game_field, by=None):
        self.last_dir = move_dir
        if move_dir in self._cannot_move_dirs(game_field):
            return
        if move_dir == Direction.UP:
            self.rect.move_ip((0, -self.step if by is None else by))
        elif move_dir == Direction.DOWN:
            self.rect.move_ip((0, self.step if by is None else by))
        elif move_dir == Direction.LEFT:
            self.rect.move_ip((-self.step if by is None else by, 0))
        elif move_dir == Direction.RIGHT:
            self.rect.move_ip((self.step if by is None else by, 0))

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
        return dirs_list

    def _cannot_move_dirs(self, game_field: GameField):
        blocked_dirs = []

        for floor in game_field.floors:
            if self.rect.colliderect(floor.rect):
                if self.rect.centery > floor.rect.bottom >= self.rect.top:
                    blocked_dirs.append(Direction.UP)
                elif self.rect.centery < floor.rect.top <= self.rect.bottom:
                    blocked_dirs.append(Direction.DOWN)

        left_walls = []
        right_walls = []
        for wall in game_field.walls:
            if self.rect.right <= wall.rect.centerx:
                right_walls.append(wall)
            if self.rect.left >= wall.rect.centerx:
                left_walls.append(wall)

        if pygame.sprite.spritecollideany(self, pygame.sprite.Group(left_walls)):
            blocked_dirs.append(Direction.LEFT)
        if pygame.sprite.spritecollideany(self, pygame.sprite.Group(right_walls)):
            blocked_dirs.append(Direction.RIGHT)

        return blocked_dirs

    def jump(self, game_field):
        if not self.is_falling and not self.is_jumping:
            self.is_jumping = True
            self.step *= 2
        if self.is_jumping:
            self.yv -= self.g * self.weight
            if self.yv > -self.jump_height and self.yv != 0:
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
