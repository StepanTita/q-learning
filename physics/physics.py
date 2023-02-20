import pygame.sprite


class Physics:
    def __init__(self, config, bounds_config):
        self.g = config['gravity']

        self.bound_w = bounds_config['width']
        self.bound_h = bounds_config['height']

    def gravity(self, sprite, game_field):
        sprite.fall(self.g, game_field)

    def bounds(self, sprite: pygame.sprite.Sprite):
        # sprite.rect.update(
        #     (sprite.rect.left % self.bound_w, sprite.rect.top % self.bound_h, sprite.rect.width, sprite.rect.height))

        sprite.rect.update(
            (max(0, sprite.rect.left), max(0, sprite.rect.top), sprite.rect.width, sprite.rect.height))

        left = sprite.rect.left
        top = sprite.rect.top
        out_bounds = False
        if sprite.rect.right > self.bound_w:
            left = self.bound_w - sprite.rect.width
        if sprite.rect.bottom > self.bound_h:
            top = self.bound_h - sprite.rect.height
            out_bounds = True
        sprite.rect.update(
            (left, top, sprite.rect.width,
             sprite.rect.height))
        return out_bounds

    def apply(self, player, game_field):
        game_state = dict()
        self.gravity(player, game_field)
        game_state['out_bounds'] = self.bounds(player)
        return game_state
