from typing import List

import pygame.sprite

from sprites.player import Player


class Physics:
    def __init__(self, config, bounds_config):
        self.g = config['gravity']

        self.bound_w = bounds_config['width']
        self.bound_h = bounds_config['height']

    def gravity(self, movers, game_field):
        for mover in movers:
            mover.fall(self.g, game_field)

    def bounds(self, movers: List[pygame.sprite.Sprite]):
        # sprite.rect.update(
        #     (sprite.rect.left % self.bound_w, sprite.rect.top % self.bound_h, sprite.rect.width, sprite.rect.height))

        out_bounds = False

        for mover in movers:
            mover.rect.update(
                (max(0, mover.rect.left), max(0, mover.rect.top), mover.rect.width, mover.rect.height))

            left = mover.rect.left
            top = mover.rect.top

            if mover.rect.right > self.bound_w:
                left = self.bound_w - mover.rect.width
            if mover.rect.bottom > self.bound_h:
                top = self.bound_h - mover.rect.height
                if isinstance(mover, Player):
                    out_bounds = True
                else:
                    mover.kill()
            mover.rect.update(
                (left, top, mover.rect.width,
                 mover.rect.height))
        return out_bounds

    def apply(self, movers, game_field):
        game_state = dict()
        self.gravity(movers, game_field)
        game_state['out_bounds'] = self.bounds(movers)
        return game_state
