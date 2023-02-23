import pygame

from constants import Direction
from field.field import GameField


class Mover:
    def __init__(self, config, g):
        self.is_falling = False

        self.step = config['step']
        self.weight = config['weight']
        self.g = g

        self.last_dir = None

    def move(self, move_dir: Direction, game_field: GameField, by=None):
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
