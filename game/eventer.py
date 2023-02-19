import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

from constants import Direction


def get_move(pressed_keys):
    # if pressed_keys[K_UP]:
    #     return Direction.UP
    if pressed_keys[K_DOWN]:
        return Direction.DOWN
    elif pressed_keys[K_LEFT]:
        return Direction.LEFT
    elif pressed_keys[K_RIGHT]:
        return Direction.RIGHT
    else:
        return Direction.STAY


class Eventer:
    def __init__(self):
        ...

    def listen(self) -> dict:
        """

        :return:
        Current state of the game loop:
        {
            "running": True
        }
        """
        running = True
        player_jump = False
        pressed_keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                ...
            elif event.type == pygame.QUIT:
                running = False

        if pressed_keys[K_SPACE]:
            player_jump = True
        return {
            'running': running,
            'player_move': get_move(pressed_keys),
            'player_jump': player_jump,
        }
