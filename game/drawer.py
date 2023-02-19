import pygame

from constants import Color, Direction

shrink_coef = 14


# TODO: refactor and remove magic constants
def dir_to_rect(last_dir, w, h):
    if last_dir == Direction.UP:
        return w // 2 - w // shrink_coef // 2, 0, w // shrink_coef, h // 2
    elif last_dir == Direction.LEFT:
        return 0, h // 2 - h // shrink_coef // 2, w // 2, h // shrink_coef
    elif last_dir == Direction.RIGHT:
        return w // 2, h // 2 - h // shrink_coef // 2, w // 2, h // shrink_coef
    elif last_dir == Direction.STAY:
        return w // 2 - w // shrink_coef // 2, h // 2 - h // shrink_coef // 2, w // shrink_coef, h // shrink_coef


class Drawer:
    def __init__(self, config):
        self.screen_dims = (config['screen']['width'], config['screen']['height'])
        self.screen = pygame.display.set_mode(self.screen_dims)

    def draw(self, game_objects):
        self.screen.fill(Color.WHITE)

        for game_obj in game_objects:
            if game_obj.shape == 'rect':
                surf, rect, last_dir = game_obj.get_state()
                if last_dir is not None:
                    surf.fill(Color.BLACK)
                    pygame.draw.rect(surf, Color.RED, pygame.Rect(*dir_to_rect(last_dir, rect.width, rect.height)))
                self.screen.blit(surf, rect)
            elif game_obj.shape == 'triangle':
                surf, tri, _ = game_obj.get_state()
                pygame.draw.polygon(surf, Color.BLACK, (tri.p1, tri.p2, tri.p3))
                self.screen.blit(surf, game_obj.rect)

        pygame.display.flip()
