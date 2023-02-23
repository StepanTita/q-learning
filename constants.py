from enum import Enum

FULL_CIRCLE_DEG = 360


class Color:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (127, 127, 127)


class Direction(Enum):
    STAY = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Action(Enum):
    STAY = 0
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    JUMP = 3


class GameStatus(Enum):
    WIN = 0
    LOST = 1
    PLAYING = 2


def action_to_direction(action):
    if action == Action.MOVE_LEFT:
        return Direction.LEFT
    elif action == Action.MOVE_RIGHT:
        return Direction.RIGHT
    elif action == Action.STAY:
        return Direction.STAY
    return None
