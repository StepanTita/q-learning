import pygame

from constants import Color, Direction
from sprites.sprite import Spriter

from collections import namedtuple

Circle = namedtuple("Circle", "pos radius")


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

    def cannot_move_dirs(self, floors, walls: pygame.sprite.Group):
        blocked_dirs = [Direction.UP]
        if pygame.sprite.spritecollideany(self, floors):
            blocked_dirs.pop(0)
            blocked_dirs.append(Direction.DOWN)
            self.is_falling = False
        elif self.is_jumping:
            blocked_dirs.pop(0)

        left_walls = []
        right_walls = []
        for wall in walls:
            if self.rect.right <= wall.rect.centerx:
                right_walls.append(wall)
            if self.rect.left >= wall.rect.centerx:
                left_walls.append(wall)

        if pygame.sprite.spritecollideany(self, pygame.sprite.Group(left_walls)):
            blocked_dirs.append(Direction.LEFT)
        if pygame.sprite.spritecollideany(self, pygame.sprite.Group(right_walls)):
            blocked_dirs.append(Direction.RIGHT)
        return blocked_dirs

    def move(self, move_dir: Direction):
        self.last_dir = move_dir
        if move_dir == Direction.UP:
            self.rect.move_ip((0, -self.step))
        elif move_dir == Direction.DOWN:
            self.rect.move_ip((0, self.step))
        elif move_dir == Direction.LEFT:
            self.rect.move_ip((-self.step, 0))
        elif move_dir == Direction.RIGHT:
            self.rect.move_ip((self.step, 0))

    def move_dirs(self, x, y):
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

    def jump(self, cannot_move_dirs):
        if self.is_jumping:
            self.yv -= self.g * self.weight
            if len(set(self.move_dirs(0, -self.yv)) & set(cannot_move_dirs)) == 0 and self.yv > -self.jump_height:
                self.rect.move_ip((0, -self.yv))
            else:
                self.yv = self.jump_height
                self.is_jumping = False
                self.step /= 2
            return
        elif not self.is_falling:
            self.is_jumping = True
            self.step *= 2

    def fall(self, g):
        self.is_falling = True
        self.rect.move_ip((0, g))

    def get_state(self):
        return self.surf, self.rect, Direction.UP if self.is_jumping else self.last_dir
