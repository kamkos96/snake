from enum import IntEnum
from typing import Tuple, TypedDict

from .colors import PygameColor, Colors

__all__ = [
    "Colors",
    "PygameColor",
    "Coordinate",
    "PxSize",
    "MovementDirection",
    "RenderInfo",
]

Coordinate = Tuple[int, int]
PxSize = Tuple[int, int]


class MovementDirection(IntEnum):
    """Enum describing the direction the Snake will move towards.
    Values are chosen so that it is easy to check if the player wants
    the Snake to go backwards - just multiply current direction by -1.
    """

    UP = -1
    DOWN = 1
    LEFT = -2
    RIGHT = 2


class RenderInfo(TypedDict):
    color: PygameColor
