import pygame.sprite

from constants import Color, FULL_CIRCLE_DEG
from geometry.triangle import make_triangle, offset_triangle
from sprites.sprite import Spriter


class Spike(pygame.sprite.Sprite, Spriter):
    def __init__(self, config):
        pygame.sprite.Sprite.__init__(self)

        self.surf = pygame.Surface((2 * config['scale'], 2 * config['scale']))
        self.surf.fill(Color.WHITE)
        self.rect = self.surf.get_rect()
        self.shape = config['shape']

        self.rect.update(config['x'], config['y'], self.surf.get_width(), self.surf.get_height())

        self.scale = config['scale']
        self.internal_angle = config['internal_angle']
        self.rotation = config['rotation']
        self.rotor = config.get('rotor', False)
        self.angle = config.get('angle', 0)

        self.tri = offset_triangle(make_triangle(self.scale, self.internal_angle, self.rotation),
                                   self.scale, self.scale)

    def rotate(self):
        if not self.rotor:
            return
        self.surf.fill(Color.WHITE)
        self.rotation = (self.rotation + self.angle) % FULL_CIRCLE_DEG
        self.tri = offset_triangle(make_triangle(self.scale, self.internal_angle, self.rotation),
                                   self.scale, self.scale)

    def get_state(self):
        return self.surf, self.tri, None
